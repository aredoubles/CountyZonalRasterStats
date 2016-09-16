%matplotlib inline
import pandas as pd
from sklearn import linear_model, preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import random
import numpy as np


barnstable = pd.read_csv('barnstable.csv')

# barnstable.plot(x='Year', y='LymeCases', kind='scatter')

X = barnstable[[2, 3]]   # Year, Bio01
X[[0]] = preprocessing.scale(barnstable[[2]])  # Standardizes variables
X[[1]] = preprocessing.scale(barnstable[[3]])  # Center on mean, scale to var
# X = barnstable[[2]]     # Year only
y = barnstable[[1]]     # LymeCases
X = X.drop(15)
y = y.drop(15)

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
# MSE train: 1124.252, test: 2212.719
print('R^2 train: %.3f, test: %.3f' % (
        r2_score(y_train, y_train_pred),
        r2_score(y_test, y_test_pred)))
# R^2 train: 0.446, test: 0.332

y_2015 = slr.predict()
