from flask import Flask, jsonify
from pymongo import MongoClient
import requests

app = Flask(__name__)

# Function to fetch data from Alpha Vantage API
def get_data():
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=YOUR_API_KEY'
    r = requests.get(url)
    data = r.json()
    return data

# Function to update MongoDB database
def update_database(data):
    # Connect to the MongoDB database
    client = MongoClient('mongodb+srv://USERNAME:PASSWORD@cluster0.mongodb.net/my_database?retryWrites=true&w=majority')
    db = client['my_database']
    collection = db['my_collection']

    # Check if the collection exists, if not, create it
    if 'my_collection' not in db.list_collection_names():
        db.create_collection('my_collection')
# Iterate over the data and insert it into the database
    for date, values in data['Time Series (Daily)'].items():
        # Prepare the document
        document = {
            'date': date,
            'open': values['1. open'],
            'high': values['2. high'],
            'low': values['3. low'],
            'close': values['4. close'],
            'volume': values['5. volume']
        }
        # Check if the document already exists
        if collection.find_one({'date': date}) is None:
            # Insert the document into the collection
            collection.insert_one(document)

@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    data = get_data()
    return jsonify(data)

@app.route('/update-database', methods=['GET'])
def update_db():
    data = get_data()
    update_database(data)
    return jsonify({'message': 'Database updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)
