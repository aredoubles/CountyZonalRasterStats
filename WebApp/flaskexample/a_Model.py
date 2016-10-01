def ModelIt(countyid):
    #in_month = len(births)
    #print 'The number born is %i' % in_month

    import pandas as pd
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.externals import joblib
    from sqlalchemy import create_engine
    from sqlalchemy_utils import database_exists, create_database
    import psycopg2
    import random
    import numpy as np

    user = 'rogershaw'
    host = 'localhost'
    dbname = 'lymeforecast'
    db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
    con = None
    con = psycopg2.connect(database = dbname, user = user)

    quoted = '{}{}{}'.format("'", countyid, "'")
    querycounty = 'SELECT * FROM grandscale WHERE county = ' + quoted
    thiscounty = pd.read_sql_query(querycounty, con)


    # X should drop columns: 0, 2, 3 (24 total columns)
    X = thiscounty.drop(thiscounty.columns[[0,25,26]], axis=1)
    #futureX = X.ix[15]
    #X = X.drop([15])

    # Headers lost on this scaling step:
    #Xcol = X.columns
    #X = pd.DataFrame(preprocessing.scale(X), columns = Xcol)
    futureX = X.ix[15]
    #futureX = preprocessing.scale(futureX)
    y = thiscounty[[26]]     # LymeCases
    #PredropX = X

    '''Random Forest Regressor'''

    #with open('flaskexample/rf_sqrt.pickle', 'rb') as f:
        #trees = pickle.load(f)

    f = 'flaskexample/rf.jblb'
    trees = joblib.load(f)

    predict15 = trees.predict(futureX.reshape(1,-1))
    #predict15 = trees.predict(futureX)
    preresult = predict15[0]
    result = int(preresult*preresult)

    print result
    return result

def DrawCis(countyid):
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlalchemy_utils import database_exists, create_database
    import psycopg2
    import numpy as np

    user = 'rogershaw'
    host = 'localhost'
    dbname = 'lymeforecast'
    db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
    con = None
    con = psycopg2.connect(database = dbname, user = user)

    quoted = '{}{}{}'.format("'", countyid, "'")
    querycounty = 'SELECT * FROM predict15 WHERE county = ' + quoted
    thiscounty = pd.read_sql_query(querycounty, con)

    #predict15 = pd.read_csv('flaskexample/static/predict15.csv', index_col = 'county')
    #thiscounty = predict15.ix[countyid]

    '''Extract 2015 and 2016 values, or just pass on array here?'''
    result = thiscounty['lymecasespred']

    return result
