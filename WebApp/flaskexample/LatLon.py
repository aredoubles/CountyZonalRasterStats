def LatLon(countyid):
    import pandas as pd
    import numpy as np
    from sqlalchemy import create_engine
    from sqlalchemy_utils import database_exists, create_database
    import psycopg2

    dbname = 'lymeforecast'
    username = 'rogershaw'
    engine = create_engine('postgres://%s@localhost/%s' % (username, dbname))

    con = None
    con = psycopg2.connect(database=dbname, user=username)


    quoter = '{}{}{}'.format("'", countyid, "'")
    countyfind = '''SELECT lat, lon FROM grandtable WHERE county = ''' + quoter
    thiscounty = pd.read_sql_query(countyfind, con)

    lat = thiscounty.ix[0][0]
    lon = thiscounty.ix[0][1]

    coords = '{}{}{}'.format(lat, ", ", lon)

    return coords
