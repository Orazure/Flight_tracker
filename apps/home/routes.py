# -*- encoding: utf-8 -*-
from apps.home import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
from datetime import datetime, timedelta
from apps.DAL.flights import FlightDAL
from apps.DAL.live_flight import LiveFlightDAL
from apps.DAL.airport import AirportDAL
from apps.configuration import SUPPORTED_FLIGHTS
from apps.DAL.dataFromMysql import Database
from apps.celery.worker import send_email
from apps.authentication.models import Users
import requests,random

@blueprint.route("/index", methods=["GET", "POST"])
@login_required
def index():
    dal = FlightDAL()
    data = []
    if request.method == "POST":
        pippo = request.form.to_dict()
        # si la donnée dans data correspond à ceux dans SUPPORTED_FLIGHTS alors je retourne la valeur de la clé
        for a in pippo["data"]:
            if a.isdigit():
                test = SUPPORTED_FLIGHTS[int(a)].values()
                dep_iata = [d["dep_icao"] for d in test]
                dep_iata = dep_iata[0]
                arr_iata = [d["arr_icao"] for d in test]
                arr_iata = arr_iata[0]
                if pippo.get("heure"):
                    filter_date = datetime.now()

                    filter_date = filter_date.replace(
                        hour=int(pippo["heure"]), minute=int(pippo["minute"])
                    )

                    print(filter_date)
                    flightsData = dal.get_flights_from_icao(
                        str(dep_iata), str(arr_iata), filter_date
                    )
                else:
                    flightsData = dal.get_flights_from_icao(
                        str(dep_iata), str(arr_iata)
                    )
                # print(flightsData)
                data.append(flightsData)
        return jsonify(data)

    # dal.get_flights_from_iata()
    # Extract the current page name
    segment = get_segment(request)

    return render_template("home/index.html", segment="index")


@blueprint.route("/getFlight")
@login_required
def getFlight():
    date = datetime.now()
    # date minus 15 minutes
    dateiso_minus = date - timedelta(minutes=15)
    print(dateiso_minus)
    return requests.get(f"http://impossibly.fr:1026/v2/entities?type=LiveFlight&q=last_update>{dateiso_minus.isoformat()};last_update<{date.isoformat()}").text


@blueprint.route("/billing", methods=["GET", "POST"])
@login_required
def stats():
    Mysql = Database()
    dropbox = Mysql.query(
        "SELECT DISTINCT(x002f.attrValue) FROM flight_tracker.x002f WHERE entityType = 'Flight' AND attrName='airline_iata'"
    )
    # remove (',') from the list dropbox
    dropbox = [x[0] for x in dropbox]
    temp = []
    data = []
    data_graph = Mysql.query(
        "SELECT x002f.entityId,recvTime FROM flight_tracker.x002f WHERE entityType = 'Flight' AND attrName='delayed' AND attrValue!='null';"
    )
    # remove duplicates entityId
    for x in data_graph:
        if x[0] not in temp:
            temp.append(x[0])
            data.append(x)
    # count the number of flight by month
    values = [random.randint(1, 5) for x in range(1, 13)]
    for flight in data:
        date = datetime.strptime(flight[1], "%m/%d/%Y %H:%M:%S")
        values[date.month - 1] += 1


    #request get with nodered to get the data
    if request.method == "POST":
        pippo = request.form.to_dict()
        data=pippo["data"]
        # add data to a string request 
        pippo="SELECT COUNT(DISTINCT(entityId)) FROM flight_tracker.x002f WHERE attrName = 'airline_iata' and attrValue='"+data+"' AND entityID IN (SELECT DISTINCT(x002f.entityId) FROM flight_tracker.x002f WHERE entityType = 'Flight' AND attrValue!='null') GROUP BY attrValue"
        pippo_delayed="SELECT COUNT(DISTINCT(entityId)) FROM flight_tracker.x002f WHERE attrName = 'airline_iata' and attrValue='"+data+"' AND entityID IN (SELECT DISTINCT(x002f.entityId) FROM flight_tracker.x002f WHERE entityType = 'Flight' AND attrName='delayed' AND attrValue='null') GROUP BY attrValue"
        number_not_delayed = Mysql.query(pippo)
        number_delayed = Mysql.query(pippo_delayed)
        number_delayed=number_delayed[0][0]
        number_not_delayed=number_not_delayed[0][0]
        return jsonify({"number_delayed":number_delayed,"number_not_delayed":number_not_delayed})

    return render_template(
        "home/billing.html", segment="billing", dropbox=dropbox, chartData=values
    )


@blueprint.route('/getAirline', methods=["GET", "POST"])
@login_required
def getArline():
    dal = FlightDAL()
    if request.method == "POST":
        pippo = request.form.to_dict()
        # si la donnée dans data correspond à ceux dans SUPPORTED_FLIGHTS alors je retourne la valeur de la clé
        print(pippo["data"])
        pippo=dal.get_airline_from_airline_iata(pippo["data"])
        return jsonify(pippo)
    return "ok"


@blueprint.route("/<template>")
@login_required
def route_template(template):

    try:

        if not template.endswith(".html"):
            template += ".html"

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template("home/page-404.html"), 404

    except:
        return render_template("home/page-500.html"), 500


@blueprint.post("/notify/delay")
def notify_delay():
    data = request.json.get("data", [])[0]
    dal = AirportDAL()
    arr_airport = dal.get_airport_from_id(data.get("arrivesToAirport"), "keyValues")
    dep_airport = dal.get_airport_from_id(data.get("departsFromAirport"), "keyValues")
    msg = f"The flight {data.get('flightNumber')} from {dep_airport.get('name')} to {arr_airport.get('name')} is delayed by {data.get('delayed')} minutes"
    print(Users.query.all())
    for user in Users.query.all():
        # send notification to user
        print(f"Send email to {user.email}")
        send_email.delay(
            user.email, msg, f"{data.get('flightNumber')} has been delayed"
        )
    return "ok"


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split("/")[-1]

        if segment == "":
            segment = "index"

        return segment

    except:
        return None
