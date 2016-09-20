from rasterstats import zonal_stats
import pandas as pd
import json
from pandas.io.json import json_normalize
import time
from path import path
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

dbname = 'lymeforecast'
username = 'rogershaw'
engine = create_engine('postgres://%s@localhost/%s' % (username, dbname))

con = None
con = psycopg2.connect(database=dbname, user=username)

#f = 'Population/Rasters/gpw-v4-population-count_2000.tif'
bpath = path('Population/Rasters')
for f in bpath.files('*.tif'):
    print '{} {} {}'.format(time.ctime(), f, 'zoning in progress...')
    zonesum = zonal_stats('Counties/tl_2016_us_county.shp',
                          f, stats='mean', geojson_out=True)
    print '{} {} {}'.format(time.ctime(), f, 'zoning done!')
    print '{} {} {}'.format(time.ctime(), f, 'flattening in progress...')
    flatson = json_normalize(zonesum)
    print '{} {} {}'.format(time.ctime(), f, 'flattening done!')
    slimson = flatson[[17, 19, 20]]
    slimson.columns = ['Name', 'State', 'Mean']
    slimson['CtyID'] = slimson['Name'] + slimson['State'].apply(str)
    slimson = slimson.set_index('CtyID')
    fname = '{}{}{}{}'.format('Population/', 'pop', str(f[-8:-4]), '.csv')
    slimson.to_csv(fname, encoding='utf-8')
    namesql = '{}{}{}'.format('populations.', 'pop', str(f[-8:-4]))
    slimson.to_sql(namesql, engine, if_exists='replace')
    print '{} {} {} {} {}'.format(time.ctime(), f, 'flattened into', fname, '!')
