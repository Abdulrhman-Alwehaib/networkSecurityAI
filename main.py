from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DATAValidation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DATAVALIDATIONConfig
from networksecurity.entity.config_entity import TrainingPiplineConfig
import sys


if __name__ == "__main__":
    try:
        trainingPiplineconfigObj = TrainingPiplineConfig()
        dataIngestionconfigObj = DataIngestionConfig(trainingPiplineconfigObj)
        dataIngestionObj = DataIngestion(dataIngestionconfigObj)
        logging.info("Initiate the data ingestion")
        dataIngestionArtifacts = dataIngestionObj.initiateDataIngestion()
        logging.info("DATA INGESTION COMPLETED!")
        print(dataIngestionArtifacts)
        dataValidationConfig = DATAVALIDATIONConfig(trainingPiplineconfigObj)
        data_Validation = DATAValidation(dataIngestionArtifacts,dataValidationConfig)
        dataValidationArtifact = data_Validation.initiateDataValidation()
        print(dataValidationArtifact)
        logging.info("DATA Validation COMPLETED!")


    except Exception as e:
        raise NetworkSecurityException(e,sys)
