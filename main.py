from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPiplineConfig
import sys


if __name__ == "__main__":
    try:
        trainingPiplineconfigObj = TrainingPiplineConfig()
        dataIngestionconfigObj = DataIngestionConfig(trainingPiplineconfigObj)
        dataIngestionObj = DataIngestion(dataIngestionconfigObj)
        logging.info("Initiate the data ingestion")
        dataIngestionArtifacts = dataIngestionObj.initiateDataIngestion()
        print(dataIngestionArtifacts)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
