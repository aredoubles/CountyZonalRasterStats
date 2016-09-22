def ModelIt(countyid):
    #in_month = len(births)
    #print 'The number born is %i' % in_month

    import pandas as pd
    from sklearn import linear_model, preprocessing, svm
    from sklearn.linear_model import LinearRegression, Ridge, Lasso, LassoLars, ElasticNet
    from sklearn.cross_validation import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import r2_score
    from sklearn.metrics import mean_squared_error
    from sqlalchemy import create_engine
    from sqlalchemy_utils import database_exists, create_database
    import psycopg2
    import random
    import numpy as np
    import pickle

    user = 'rogershaw'
    host = 'localhost'
    dbname = 'lymeforecast'
    db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
    con = None
    con = psycopg2.connect(database = dbname, user = user)

    quoted = '{}{}{}'.format("'", countyid, "'")
    querycounty = 'SELECT * FROM grandtable WHERE county = ' + quoted
    thiscounty = pd.read_sql_query(querycounty, con)


    # X should drop columns: 0, 2, 3 (24 total columns)
    X = thiscounty.drop(thiscounty.columns[[0,2,3]], axis=1)
    futureX = X.ix[15]
    X = X.drop([15])

    # Headers lost on this scaling step:
    Xcol = X.columns
    X = pd.DataFrame(preprocessing.scale(X), columns = Xcol)
    y = thiscounty[[2]]     # LymeCases
    #PredropX = X

    '''Random Forest Regressor'''

    with open('flaskexample/rf.pickle', 'rb') as f:
        trees = pickle.load(f)

    predict15 = trees.predict(futureX.reshape(1,-1))
    result = int(predict15[0])

    print result
    return result
