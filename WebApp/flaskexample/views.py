from flask import render_template, request
from flaskexample import app
from a_Model import ModelIt
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
    return render_template("input.html")


@app.route('/db')
def birth_page():
    sql_query = """
                SELECT * FROM grandtable;
                """
    query_results = pd.read_sql_query(sql_query, con)
    feats = ""
    for i in range(0, 2):
        feats += query_results.iloc[i]['variable']
        feats += "<br>"
    return feats


@app.route('/db_fancy')
def cesareans_page_fancy():
    sql_query = """
               SELECT * FROM "counties.barnstable";
                """
    query_results = pd.read_sql_query(sql_query, con)
    feats = []
    for i in range(0, query_results.shape[0]):
        feats.append(dict(index=query_results.iloc[i]['variable'], attendant=query_results.iloc[
                     i][2000], birth_month=query_results.iloc[i][2001]))
    return render_template('cesareans.html', births=births)


@app.route('/input')
def cesareans_input():
    return render_template("input.html")


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
