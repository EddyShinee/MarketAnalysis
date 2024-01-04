#######################################################################################################################################
# connector = CommonMongoDBConnector.CommonMongoDBConnector('mongodb://localhost:27017/')
# # Đẩy DataFrame Data lên MongoDB
# connector.dataframe_to_mongodb(data, 'Cole', 'Bollinger_Bands')
from pymongo import MongoClient
import pandas as pd


class CommonMongoDBConnector:
    def __init__(self, uri):
        self.client = MongoClient(uri)

    def dataframe_to_mongodb(self, df, database_name, collection_name):
        # Kết nối tới database và collection
        db = self.client[database_name]
        collection = db[collection_name]

        # Chuyển DataFrame thành dictionary và đẩy lên MongoDB
        records = df.to_dict('records')
        collection.insert_many(records)

    def close_connection(self):
        self.client.close()
