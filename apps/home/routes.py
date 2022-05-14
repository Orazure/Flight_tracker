# -*- encoding: utf-8 -*-

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound

from apps.DAL.flights import FlightDAL
from apps.configuration import SUPPORTED_FLIGHTS, SUPPORTED_AIRPORTS

@blueprint.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    dal = FlightDAL()
    listeData=[]
    if request.method == 'POST':
        pippo =  request.form.to_dict()
        print(pippo['data'])
        # si la donnée dans data correspond à ceux dans SUPPORTED_FLIGHTS alors je retourne la valeur de la clé
        for a in pippo['data']:
            if a.isdigit():
                test=SUPPORTED_FLIGHTS[int(a)].values()
                dep_iata=[d['dep_iata'] for d in test]
                #remove [] in dep_iata
                dep_iata=dep_iata[0]
                dep_iata=str(dep_iata)
                print(dep_iata)
                arr_iata=[d['arr_iata'] for d in test]
                arr_iata=arr_iata[0]
                arr_iata=str(arr_iata)
                print(arr_iata)
            
                test=dal.get_flights_from_iata(str(dep_iata),str(arr_iata))
                print(dal.get_flights_from_iata('CDG', 'JFK'))
                print(test)
        # dal.get_flights_from_iata()
    # Extract the current page name
    segment = get_segment(request)
    
    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

# @blueprint.route('/search/data')
# @login_required
# def dataFlight():

#     return render_template('home/index.html', segment='index')

# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
