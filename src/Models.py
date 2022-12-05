#Import libraries
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn import tree


#Load data
df = pd.read_csv("yield_and_climate_data_cleaned.csv")


#Linear Regression

#using all variables except for snow_thickness_lwe
variables = ['cloud_cover', 'snow_thickness', 'vapour_pressure','2m_temperature', '10m_wind_speed', '2m_dewpoint_temperature']

#Linear model using annually aggregated variables

Y = df["Yield"]
X = df[variables] 
#split data into train and test data
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3, random_state = 1)
lr1 = LinearRegression()
lr1.fit(X_train, y_train)
print(lr1.score(X_test, y_test))


#Linear model using 3 groups of variables
cols = [variable+"_g"+str(i) for variable in variables for i in range(3)]

Y = df["Yield"]
X = df[cols] 
#split data into train and test data
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3, random_state = 1)
lr2 = LinearRegression()
lr2.fit(X_train, y_train)
print(lr2.score(X_test, y_test))


#SVR

Y = df["Yield"]
X = df[variables] 
#split data into train and test data
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3, random_state = 1)
svr1 = SVR(kernel='rbf')
svr1.fit(X_train, y_train)
print(svr1.score(X_test, y_test))


#Tree based
 
Y = df["Yield"]
X = df[variables] 
#split data into train and test data
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3, random_state = 1)
tr1 = tree.DecisionTreeRegressor()
tr1.fit(X_train, y_train)
print(tr1.score(X_test, y_test))
