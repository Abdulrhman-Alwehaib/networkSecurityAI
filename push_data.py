import os
import sys
import json
#certify library provides root certificates for Python apps to verify SSL/TLS connections 
import certifi
import pandas as pd
import numpy as np
import pymongo
import pymongo.mongo_client
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from dotenv import load_dotenv
load_dotenv()

#load_dotenv() (from python-dotenv) manually loads variables from a .env file into os.environ
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

#certifi.where() retrieves the path (file path to the CA certificate bundle) to certify’s trusted root certificates
ca = certifi.where()

#ELT pipline
class NetworkDataETL():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def cvToJsonConversion(self,filePath):
        try:
            data = pd.read_csv(filePath)
            data.reset_index(drop=True,inplace=True)
            records = list(json.loads((data.T.to_json())).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def insertDataToMongoDB(self,records,database,collection):
        try:
            self.mongoClient = pymongo.MongoClient(MONGO_DB_URL)
            #database refers to a MongoDB database (a logical container for collections) and not a Cluster
            #just names assigments
            self.database = self.mongoClient[database]
            self.collection = self.database[collection]

            self.collection.insert_many(records)
            return(len(records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__ == "__main__":
    FILEPATH = "NetworkData\phisingData.csv"
    DATABASE = "AbdulrhmanDataBase"
    COLLECTION = "NetworkData"
    NetworkDataObj = NetworkDataETL()
    records = NetworkDataObj.cvToJsonConversion(FILEPATH)
    numOfRecords = NetworkDataObj.insertDataToMongoDB(records=records,database=DATABASE,collection=COLLECTION)
    print(numOfRecords)
