from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import os,sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer,SimpleImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipline import TARGET_COLUMN
from networksecurity.constant.training_pipline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (
    DataValidationArtifact,DATATransformationArtifact
)
from networksecurity.utils.main_utils import(
    saveNumpyArray,SaveObjectAsPickleFile,readData
)

from networksecurity.entity.config_entity import DataTransformationConfig

#start the Data Transformation Pipline

class DataTransfomration:
    def __init__(self,dataValidationArtifict:DataValidationArtifact,
                 dataTransformationConfig:DataTransformationConfig):
        try:
            self.dataValidationArtifact = dataValidationArtifict
            self.dataTransformationConfig = dataTransformationConfig
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    @staticmethod
    def getDataTransformerImputerObj() ->Pipeline:
        logging.info("Entered the get data trnasfomer Object")

        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor:Pipeline = Pipeline([("Imputer",imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)



    def inititeDataTransformation(self) -> DataValidationArtifact:
        logging.info("Entered Data Transformation Stage")
        try:
            logging.info("Starting Data Transformation")
            trainDf = readData(self.dataValidationArtifact.valid_train_file_path)
            testDf = readData(self.dataValidationArtifact.valid_test_file_path)

            #training DataFrame (independent and dependent Features!)
            inputFeatureTrainDF = trainDf.drop(columns=[TARGET_COLUMN],axis=1)
            targetFeatureTrainDF = trainDf[TARGET_COLUMN]
            targetFeatureTrainDF = targetFeatureTrainDF.replace(-1,0)

            #training DataFrame (independent and dependent Features!)
            inputFeatureTestDF = testDf.drop(columns=[TARGET_COLUMN],axis=1)
            targetFeatureTestDF = testDf[TARGET_COLUMN]
            targetFeatureTestDF = targetFeatureTestDF.replace(-1,0)


            preprocessor = DataTransfomration.getDataTransformerImputerObj()
            
            preproccessorObj = preprocessor.fit(inputFeatureTrainDF)
            transformedInputTrainFeature = preproccessorObj.transform(inputFeatureTrainDF)
            transformedInputTestFeature = preproccessorObj.transform(inputFeatureTestDF)

            trainArr = np.c_[transformedInputTrainFeature,np.array(targetFeatureTrainDF)]
            testArr = np.c_[transformedInputTestFeature,np.array(targetFeatureTestDF)]
            
            saveNumpyArray(self.dataTransformationConfig.DataTransformedTrainPath,trainArr)
            saveNumpyArray(self.dataTransformationConfig.DataTransformedTestPath,testArr)
            SaveObjectAsPickleFile(self.dataTransformationConfig.dataTransformationObj,preproccessorObj)


            #preparing artifacts

            dataTransformationArtifact = DATATransformationArtifact(
                transformationObjectFilePAth = self.dataTransformationConfig.dataTransformationObj,
                transformedTrainFilePath = self.dataTransformationConfig.DataTransformedTrainPath,
                transformedTestFilePath = self.dataTransformationConfig.DataTransformedTestPath
            )

            return dataTransformationArtifact



        except Exception as e:
            raise NetworkSecurityException(e,sys)
        