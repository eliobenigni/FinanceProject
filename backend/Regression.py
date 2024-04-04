from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
from CleanData import data

def model_training(data):
    df = data
    df['close'] = df['close'].shift(-1)
    df = df.dropna()
    X = df.drop('close', axis=1)
    y = df['close']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    model = linear_model.LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    return mse