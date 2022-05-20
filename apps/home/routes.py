# -*- encoding: utf-8 -*-

from apps.home import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
import requests
from datetime import datetime

from apps.DAL.flights import FlightDAL
from apps.DAL.live_flight import LiveFlightDAL
from apps.DAL.airport import AirportDAL
from apps.configuration import SUPPORTED_FLIGHTS, SUPPORTED_AIRPORTS
from apps.celery.worker import send_email
from apps.authentication.models import Users


@blueprint.route("/index", methods=["GET", "POST"])
@login_required
def index():
    dal = FlightDAL()
    flights = LiveFlightDAL()
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
    return requests.get("http://impossibly.fr:1026/v2/entities?types=LiveFlight").text


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


# @blueprint.route('/search/data')
# @login_required
# def dataFlight():

#     return render_template('home/index.html', segment='index')

# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split("/")[-1]

        if segment == "":
            segment = "index"

        return segment

    except:
        return None
