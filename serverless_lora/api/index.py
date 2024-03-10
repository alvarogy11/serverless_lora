from flask import Flask, request, jsonify
from flask_cors import CORS
import  pymongo
from dotenv import load_dotenv
import os
import certifi

load_dotenv()
mongo_string = os.getenv("MONGO_KEY")

app = Flask(__name__)
CORS(app) 

# Connect to MongoDB

@app.route('/api/posts', methods=['POST'])
def create_post():
    
    data = request.json
    
    connection = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
    db = 'GeoLora'  # Replace 'your_database_name' with your actual database name
    collection = 'Measures'  # Replace 'your_collection_name' with your actual collection name
    connection[db][collection].insert_one(data)

    return 'OK'

@app.route('/api/posts2', methods=['POST'])
def create_post2():
    
    data = request.json
    
    connection = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
    db = 'GeoLora'  # Replace 'your_database_name' with your actual database name
    collection = 'Measures_2'  # Replace 'your_collection_name' with your actual collection name
    connection[db][collection].insert_one(data)

    return 'OK'

@app.route('/api/pruebas', methods=['POST'])
def post_pruebas():
    
    data = request.json
    
    connection = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
    db = 'GeoLora'  # Replace 'your_database_name' with your actual database name
    collection = 'pruebas'  # Replace 'your_collection_name' with your actual collection name
    connection[db][collection].insert_one(data)

    return 'OK'

@app.route('/api/test', methods=['GET'])
def test():
    
    return 'OK'

if __name__ == '__main__':
    app.run()
    # Connect to MongoDB
    