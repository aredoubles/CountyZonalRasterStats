def ModelIt(fromUser  = 'Default', births = []):
  #in_month = len(births)
  #print 'The number born is %i' % in_month

  from sklearn import linear_model, preprocessing
  from sklearn.linear_model import LinearRegression
  from sklearn.cross_validation import train_test_split
  from sklearn.metrics import r2_score
  from sklearn.metrics import mean_squared_error
  from sqlalchemy import create_engine
  from sqlalchemy_utils import database_exists, create_database
  import pandas as pd
  import psycopg2

  user = 'rogershaw'
  host = 'localhost'
  dbname = 'lymeforecast'
  db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
  con = None
  con = psycopg2.connect(database = dbname, user = user)

  query = '''SELECT "Year", "LymeCases", "Bio01" FROM "counties.barnstable"; '''
  barnstable = pd.read_sql_query(query,con)

  X = barnstable[[0,2]]   # Year, Bio01
  X[[0]] = preprocessing.scale(barnstable[[0]])   #Standardizes variables
  X[[1]] = preprocessing.scale(barnstable[[2]])   #Center on mean, scale to var
  PredropX = X
  X = X.drop(15)
  # X = barnstable[[2]]     # Year only
  y = barnstable[[1]]
  y = y.drop(15)
  '''
  OLD, SIMPLE LINEAR REGRESSION
  ols = linear_model.LinearRegression()
  model = ols.fit(X, y)
  model.coef_                             # Coefficients/weights?
  R2 = model.score(X, y)             # R^2 score
  '''

  X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=0)

  slr = LinearRegression()

  slr.fit(X_train, y_train)
  y_train_pred = slr.predict(X_train)
  y_test_pred = slr.predict(X_test)

  result = slr.predict(PredropX.ix[15])
  result = result[0][0]
  result = int(result)
  '''
  OLD RESULT
  result = model.predict(PredropX.ix[15])
  result = result[0][0]
  result = int(result)
  '''

  print result
  if fromUser != 'Default':
    return result
  else:
    return 'check your input'
