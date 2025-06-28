from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

#Configuration of Data Ingestion Config

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import os
import sys
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
import pandas as pd
import certifi
ca = certifi.where()
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

#reading from mongoDB

class DataIngestion:
    def __init__(self,dataIngestionConfig:DataIngestionConfig):
        try:
            self.dataIngestionConfig = dataIngestionConfig

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def exportCollectionAsDataFrame(self):
        """
        READ THE DATA FROM MONGODB (QUERY)
        """
        try:
            dataBaseName = self.dataIngestionConfig.database_name
            collectionName = self.dataIngestionConfig.collection_name
            self.mongoClient = pymongo.MongoClient(MONGO_DB_URL,tlsCAFile=ca)
            collection = self.mongoClient[dataBaseName][collectionName]
            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df.drop(columns=["_id"],axis=1,inplace=True)
            
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            NetworkSecurityException(e,sys)

    def exportDataToFeatureStore(self,DF:pd.DataFrame):
        try:
            featureStoreFilePath = self.dataIngestionConfig.feature_store_file_path

            dirPath = os.path.dirname(featureStoreFilePath) #os.path.dirname("/data/raw/file.csv") → "/data/raw"
            os.makedirs(dirPath,exist_ok=True)
            DF.to_csv(featureStoreFilePath,index=False,header=True)
            return DF
        except Exception as e:
            NetworkSecurityException(e,sys)
    
    def splitDataTrainTest(self,DF:pd.DataFrame):
        try:
            trainSet,testSet= train_test_split(
                DF,test_size=self.dataIngestionConfig.train_test_split_ratio
            )

            logging.info("Performed train test split")

            dirPath = os.path.dirname(self.dataIngestionConfig.training_file_path)
            os.makedirs(dirPath,exist_ok=True)

            

            trainSet = pd.DataFrame(trainSet)
            testSet = pd.DataFrame(testSet)

            trainSet.to_csv(
                self.dataIngestionConfig.training_file_path,index=False,header=True
            )
            testSet.to_csv(
                self.dataIngestionConfig.test_file_path,index=False,header=True
            )
            #"exporting" means outputting data from your program into a file/format
            logging.info("Exported train and test file path")
        except Exception as e:
            NetworkSecurityException(e,sys)

    #initiat Data ingestion
    def initiateDataIngestion(self):
        try:
            dataFrame = self.exportCollectionAsDataFrame()
            dataFrame = self.exportDataToFeatureStore(dataFrame)
            self.splitDataTrainTest(dataFrame)

            data_ingestion_artifact = DataIngestionArtifact(
                trainingFilePath=self.dataIngestionConfig.training_file_path,
                testFilePath=self.dataIngestionConfig.test_file_path)
            
            return data_ingestion_artifact
        except Exception as e:
            NetworkSecurityException(e,sys)