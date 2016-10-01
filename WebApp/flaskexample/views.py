from flask import render_template, request
from flaskexample import app
from a_Model import ModelIt, DrawCis
from LatLon import LatLon
from ggplotting import PlotIt, OverPlot
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

    #the_result = ModelIt(countyid)
    the_result = DrawCis(countyid)
    plotPng = OverPlot(countyid, countyname, the_result)
    pred15 = int(the_result[0])
    pred16 = int(the_result[1])
    return render_template("output.html", countyid=countyid, countyname=countyname, plotPng=plotPng, pred15=pred15, pred16=pred16)


@app.route('/about')
def about():
    return render_template("about.html")
