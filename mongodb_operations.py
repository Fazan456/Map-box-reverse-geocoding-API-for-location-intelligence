from pymongo import MongoClient
from datetime import datetime, timedelta
import pandas as pd
import config

def connect_to_mongodb():
    client = MongoClient(config.MONGODB_CONNECTION_STRING)
    database = client[config.MONGODB_DB_NAME]
    return client, database

def close_mongodb_connection(client):
    client.close()

def get_newly_onboarded_sites():
    client, db = connect_to_mongodb()

    aggregation_results = {}
    for collection_name in config.MONGODB_COLLECTIONS:
        pipeline = [
            {
                '$match': {
                    'created_date': {
                        '$gte': datetime.now() - timedelta(days=30),
                        '$lt': datetime.now()
                    }
                }
            },
            {
                '$group': {
                    '_id': '$reference_id', 
                    'latitude': {'$first': '$latitude'},  
                    'longitude': {'$first': '$longitude'} 
                }
            },
            {
                '$project': {
                    '_id': 0, 
                    'reference_id': '$_id',  
                    'latitude': 1,
                    'longitude': 1
                }
            }
        ]

        collection = db[collection_name]
        newly_onboarded_sites = list(collection.aggregate(pipeline))
        aggregation_results[collection_name] = pd.DataFrame(newly_onboarded_sites)

    close_mongodb_connection(client)
    return aggregation_results
