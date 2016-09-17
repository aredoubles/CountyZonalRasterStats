%matplotlib inline
import pandas as pd
from sklearn import linear_model, preprocessing
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.cross_validation import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import random
import numpy as np


barnstable = pd.read_csv('barnstable.csv')

# barnstable.plot(x='Year', y='LymeCases', kind='scatter')

X = barnstable[[2,3,4]]   # Year, Bio01, Bio02
X[[0]] = preprocessing.scale(barnstable[[2]])  # Standardizes variables
X[[1]] = preprocessing.scale(barnstable[[3]])  # Center on mean, scale to var
X[[2]] = preprocessing.scale(barnstable[[4]])
# X = barnstable[[2]]     # Year only
y = barnstable[[1]]     # LymeCases
PredropX = X
X = X.drop(15)
y = y.drop(15)
'''Skip ahead to automated random split'''
X_train = X[0:10]
y_train = y[0:10]

X_test = X[10:]
y_test = y[10:]

ols = linear_model.LinearRegression()
model = ols.fit(X_train, y_train)
model.coef_                             # Coefficients/weights?
model.score(X_test, y_test)             # R^2 score
# Year only: R^2 = 0.23, Lyme = -13621.48 + 6.885 * Yr
model.intercept_

list(model.predict(X_test)[0:5])
list(y_test)[0:5]
((y_test - model.predict(X_test)) ** 2).sum()  # RSS
np.mean((model.predict(X_test) - y_test) ** 2)  # MSE

''''''

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=0)

slr = LinearRegression()

slr.fit(X_train, y_train)
y_train_pred = slr.predict(X_train)
y_test_pred = slr.predict(X_test)

print('MSE train: %.3f, test: %.3f' % (
        mean_squared_error(y_train, y_train_pred),
        mean_squared_error(y_test, y_test_pred)))
# MSE train: 1124.252, test: 2212.719       # Bio01
# MSE train: 1014.180, test: 2946.979       # Bio01, Bio02
print('R^2 train: %.3f, test: %.3f' % (
        r2_score(y_train, y_train_pred),
        r2_score(y_test, y_test_pred)))
# R^2 train: 0.446, test: 0.332     #Bio01
# R^2 train: 0.500, test: 0.110     #Bio01, Bio02


slr.fit(X_train, y_train).coef_
# array([[ 36.02384887,  -5.22981331]])
# array([[ 35.75486307, -10.35803815,  18.64272682]])
slr.fit(X_train, y_train).score(X_test, y_test)

result = slr.predict(PredropX.ix[15])
result = result[0][0]
result = int(result)

'''Ridge regression'''

rrc = Ridge()

rrc.fit(X_train,y_train)
y_train_pred = rrc.predict(X_train)
y_test_pred = rrc.predict(X_test)

print('MSE train: %.3f, test: %.3f' % (
        mean_squared_error(y_train, y_train_pred),
        mean_squared_error(y_test, y_test_pred)))
# MSE train: 1144.035, test: 2474.597       # Bio01
# MSE train: 1042.990, test: 2817.660       # Bio01, Bio02
print('R^2 train: %.3f, test: %.3f' % (
        r2_score(y_train, y_train_pred),
        r2_score(y_test, y_test_pred)))
# R^2 train: 0.436, test: 0.253
# R^2 train: 0.486, test: 0.149
# Worse than simple linear regression!

'''Lasso'''
lasso = Lasso(alpha=0.1)
lasso.fit(X_train, y_train)
y_train_pred = lasso.predict(X_train)
y_test_pred = lasso.predict(X_test)

print('MSE train: %.3f, test: %.3f' % (
        mean_squared_error(y_train, y_train_pred),
        mean_squared_error(y_test, y_test_pred)))
# MSE train: 1124.312, test: 2226.141
# MSE train: 1014.291, test: 2924.448
print('R^2 train: %.3f, test: %.3f' % (
        r2_score(y_train, y_train_pred),
        r2_score(y_test, y_test_pred)))
# R^2 train: 0.446, test: 0.328
# R^2 train: 0.500, test: 0.117
# Still worse than simple linear regression!
