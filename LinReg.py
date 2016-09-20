%matplotlib inline
import pandas as pd
from sklearn import linear_model, preprocessing, svm
from sklearn.linear_model import LinearRegression, Ridge, Lasso, LassoLars, ElasticNet
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import random
import numpy as np


grandtable = pd.read_csv('_grandtable.csv')

# grandtable.plot(x='Year', y='LymeCases', kind='scatter')

trainset = grandtable[grandtable.Year != 2015]
futurepredict = grandtable[grandtable.Year == 2015]

# X should drop columns: 0, 2, 3 (24 total columns)
X = trainset.drop(trainset.columns[[0,2,3]], axis=1)
futureX = futurepredict.drop(futurepredict.columns[[0,2,3]], axis=1)

X = pd.DataFrame(preprocessing.scale(X))
y = trainset[[2]]     # LymeCases
#PredropX = X

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=0)
''''''
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

slr = LinearRegression()

slr.fit(X_train, y_train)
y_train_pred = slr.predict(X_train)
y_test_pred = slr.predict(X_test)

print('MSE train: %.3f, test: %.3f' % (
        mean_squared_error(y_train, y_train_pred),
        mean_squared_error(y_test, y_test_pred)))
# MSE train: 1124.252, test: 2212.719       # Bio01
# MSE train: 1014.180, test: 2946.979       # Bio01, Bio02
# Severe overfitting with Bio1–8
# MSE train: 15121.107, test: 20063.472      # Full
print('R^2 train: %.3f, test: %.3f' % (
        r2_score(y_train, y_train_pred),
        r2_score(y_test, y_test_pred)))
# R^2 train: 0.446, test: 0.332     #Bio01
# R^2 train: 0.500, test: 0.110     #Bio01, Bio02
# Severe overfitting with Bio1–8
# R^2 train: 0.684, test: 0.128     # Full


slr.fit(X_train, y_train).coef_
# array([[ 36.02384887,  -5.22981331]])
# array([[ 35.75486307, -10.35803815,  18.64272682]])
slr.fit(X_train, y_train).score(X_test, y_test) #R^2 on test set

result = slr.predict(futureX)
#result = result[0][0]
#result = int(result)
#print result

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
# MSE train: 17178.728, test: 19720.481     # full
print('R^2 train: %.3f, test: %.3f' % (
        r2_score(y_train, y_train_pred),
        r2_score(y_test, y_test_pred)))
# R^2 train: 0.436, test: 0.253
# R^2 train: 0.486, test: 0.149
# Worse than simple linear regression!
# R^2 train: 0.641, test: 0.143     #full

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
# MSE train: 15562.842, test: 19199.434
print('R^2 train: %.3f, test: %.3f' % (
        r2_score(y_train, y_train_pred),
        r2_score(y_test, y_test_pred)))
# R^2 train: 0.446, test: 0.328
# R^2 train: 0.500, test: 0.117
# R^2 train: 0.675, test: 0.166     # full
# Still worse than simple linear regression!

'''Lasso LARS'''
lassol = LassoLars(alpha=0.1)
lassol.fit(X_train, y_train)
y_train_pred = lassol.predict(X_train)
y_test_pred = lassol.predict(X_test)

print('MSE train: %.3f, test: %.3f' % (
        mean_squared_error(y_train, y_train_pred),
        mean_squared_error(y_test, y_test_pred)))
# MSE train: 4673.540, test: 28406.077      # full
# MSE train: 17549.219, test: 19599.301     # full, all MA
print('R^2 train: %.3f, test: %.3f' % (
        r2_score(y_train, y_train_pred),
        r2_score(y_test, y_test_pred)))
# R^2 train: 0.832, test: 0.418         # full
# R^2 train: 0.633, test: 0.148         # full, all MA
# Still worse than simple linear regression!

'''ElasticNet'''
elast = ElasticNet(alpha=0.1)
elast.fit(X_train, y_train)
y_train_pred = elast.predict(X_train)
y_test_pred = elast.predict(X_test)

print('MSE train: %.3f, test: %.3f' % (
        mean_squared_error(y_train, y_train_pred),
        mean_squared_error(y_test, y_test_pred)))
# MSE train: 4673.540, test: 28406.077      # full
# MSE train: 18342.896, test: 19481.151     # full, all MA
print('R^2 train: %.3f, test: %.3f' % (
        r2_score(y_train, y_train_pred),
        r2_score(y_test, y_test_pred)))
# R^2 train: 0.832, test: 0.418         # full
# R^2 train: 0.617, test: 0.154         # full, all MA
# Still worse than simple linear regression!

'''SVM'''
sup = svm.NuSVR()
sup.fit(X_train, y_train)
y_train_pred = sup.predict(X_train)
y_test_pred = sup.predict(X_test)

print('MSE train: %.3f, test: %.3f' % (
        mean_squared_error(y_train, y_train_pred),
        mean_squared_error(y_test, y_test_pred)))
# MSE train: 53938.086, test: 22670.365
print('R^2 train: %.3f, test: %.3f' % (
        r2_score(y_train, y_train_pred),
        r2_score(y_test, y_test_pred)))
# R^2 train: -0.127, test: 0.015

'''Random Forest Regressor'''
trees = RandomForestRegressor(oob_score=True)
trees.fit(X_train, y_train)
y_train_pred = trees.predict(X_train)
y_test_pred = trees.predict(X_test)

print('MSE train: %.3f, test: %.3f' % (
        mean_squared_error(y_train, y_train_pred),
        mean_squared_error(y_test, y_test_pred)))
# MSE train: 2197.075, test: 14939.625
print('R^2 train: %.3f, test: %.3f' % (
        r2_score(y_train, y_train_pred),
        r2_score(y_test, y_test_pred)))
# R^2 train: 0.954, test: 0.351
