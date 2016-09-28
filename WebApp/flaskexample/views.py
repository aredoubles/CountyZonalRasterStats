from flask import render_template, request
from flaskexample import app
from a_Model import ModelIt
from LatLon import LatLon
from ggplotting import PlotIt
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2

user = 'rogershaw'
host = 'localhost'
dbname = 'lymeforecast'
db = create_engine('postgres://%s%s/%s' % (user, host, dbname))
con = None
con = psycopg2.connect(database=dbname, user=user)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/input')
def cesareans_input():
    return render_template("index.html")


@app.route('/output')
def cesareans_output():
    # pull 'birth_month' from input field and store it
    countyid = request.args.get('birth_month')

    if countyid[-3].isdigit() == True:
        countyname = countyid[:-3] + ' County'
    else:
        countyname = countyid[:-2] + ' County'

    the_result = ModelIt(countyid)
    plotPng = PlotIt(countyid, countyname, the_result)
    return render_template("output.html", countyid=countyid, countyname=countyname, the_result=the_result, plotPng=plotPng)


@app.route('/about')
def about():
    return render_template("about.html")
