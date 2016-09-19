import pandas as pd
from path import path
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

dbname = 'lymeforecast'
username = 'rogershaw'
engine = create_engine('postgres://%s@localhost/%s' % (username, dbname))

con = None
con = psycopg2.connect(database=dbname, user=username)

i=1
cpath = path('CountyTables')
for f in cpath.files(pattern='*.csv'):
    if i == 1:   # Seed the grand table with the first county table
        GrandTable = pd.read_csv(f)
        i += i
    else:
        newcount = pd.read_csv(f)
        GrandTable = pd.concat([GrandTable, newcount])
    # Save GrandTable to csv and sql
    GrandTable.to_csv('_grandtable.csv')
    GrandTable.to_sql('grandtable', engine, if_exists='replace')
