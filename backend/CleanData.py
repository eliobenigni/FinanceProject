import pandas as pd
import numpy as np
from flask import Flask, request, jsonify


def clean_data(data):
    df=data
   # mean = df.mean()
    df = df.dropna()
    df = df.reset_index()
    df.drop_duplicates(subset='date', keep='first', inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    
    return df

app = Flask(__name__)

@app.route('/clean', methods=['GET'])
def clean():
    df = clean_data(data)
    return df.to_json()




