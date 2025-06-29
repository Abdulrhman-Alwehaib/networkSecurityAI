from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DATAVALIDATIONConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipline import SCHEMA_FILE_PATH
#compares two datasets to check if they come from the same distribution 
from scipy.stats import ks_2samp
import pandas as pd
import os
import sys
from networksecurity.utils.main_utils import read_yaml_file,writeYampleFile

#Intial Stage
class DATAValidation:
    def __init__(self,DataIngestionArtifact:DataIngestionArtifact,
                 DataValidationConfig:DATAVALIDATIONConfig
                 ):
        
        try:
            self.dataValidationConfig = DataValidationConfig
            self.dataIngestionartifact = DataIngestionArtifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            NetworkSecurityException(e,sys)
    
    @staticmethod
    def readData(filePath)->pd.DataFrame:
        try:
            
            return pd.read_csv(filePath)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def validateNumberOfCol(self,dataframe:pd.DataFrame) ->bool:
        try:
           same = True
           report ={}
           numberOfColoumns:int = len(self._schema_config["columns"])
           logging.info(f"Required Number of coloumns: {numberOfColoumns}")
           logging.info(f"num of data coloumns: {len(dataframe.columns)}")

           if len(dataframe.columns) == numberOfColoumns:
               same = True
               report.update({"Coloumn Conformation Number":same})
               validatedReportSchema = self.dataValidationConfig.schema_validation_file_path
               writeYampleFile(validatedReportSchema,report)
              

               return same
            
           else:
                report.update({"Coloumn Conformation Number":same})
                validatedReportSchema = self.dataValidationConfig.schema_validation_file_path
                writeYampleFile(validatedReportSchema,report)
                same = False
                return same
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def ValidateNumericalColoumns(self,dataFrame:pd.DataFrame)->bool:
        try:
            sameNumericalColoumns = True
            report = {}
            expectedNumericalColoumns = self._schema_config["numerical_columns"]
            actualNumericalColoumns = list(dataFrame.columns)

            if len(expectedNumericalColoumns) == len(actualNumericalColoumns):
                report.update({"same Numerical Coloumns":sameNumericalColoumns})
                validatedReportSchema = self.dataValidationConfig.schema_validation_file_path
                writeYampleFile(validatedReportSchema,report)
                return sameNumericalColoumns
            else:
                report.update({"same Numerical Coloumns":sameNumericalColoumns})
                validatedReportSchema = self.dataValidationConfig.schema_validation_file_path
                writeYampleFile(validatedReportSchema,report)
                return sameNumericalColoumns
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def detectDatasetDrift(self,baseDf,currentDF,threshold:int = 0.05)->bool:
        try:
            status = True
            report = {}
            for column in baseDf.columns:
                d1 = baseDf[column]
                d2 = currentDF[column]
                (_,pValue) = ks_2samp(d1,d2)
                if pValue > threshold:
                    #Falied to Reject null hypothesis
                    drift_detected = False
                    status = False
                else:
                    # Reject null hypothesis
                    drift_detected = True
                
                report.update({column:{
                    "p-value:":float(pValue),
                    "drift detected":drift_detected
                }})

            drifReportFilePath = self.dataValidationConfig.drift_report_file_path

            dirPAth = os.path.dirname(drifReportFilePath)
            os.makedirs(dirPAth,exist_ok=True)
            writeYampleFile(filePath=drifReportFilePath,content=report)
            return not status
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    #initiating Data validation stage (config is a prerequists and i already done that (check earlier files))
    def initiateDataValidation(self)->DataIngestionArtifact:
        try:
            trainFilePath = self.dataIngestionartifact.trainingFilePath
            testFilePath = self.dataIngestionartifact.testFilePath

            trainDataFram:pd.DataFrame = DATAValidation.readData(trainFilePath)
            testDataFrame:pd.DataFrame = DATAValidation.readData(testFilePath)


            #Validation of number of coloumns
            statusTrain = self.validateNumberOfCol(dataframe=trainDataFram)
            if not statusTrain:
                errorMessage = f"Train DataFrame doesnt have all coloumns"
            statusTest = self.validateNumberOfCol(dataframe=testDataFrame)
            if not statusTest:
                errorMessage = f"Train DataFrame doesnt have all coloumns"

            statusNumericalColoumns = self.ValidateNumericalColoumns(trainDataFram) and self.ValidateNumericalColoumns(testDataFrame)

            if not (statusTrain and statusTest):
                raise ValueError("mismatch with number of coloumns")
            if not statusNumericalColoumns:
                raise ValueError("mismatch with numerical coloumns")
            #check dataDraft
            #better to check with a new Data and not test data (will be FIXED!)
            statusDataDrift = self.detectDatasetDrift(baseDf=trainDataFram,currentDF=testDataFrame)
            dirPathValid = os.path.dirname(self.dataValidationConfig.valid_test_file_path)
            os.makedirs(dirPathValid,exist_ok=True)
            dirPathInvalid = os.path.dirname(self.dataValidationConfig.invalid_test_file_path)
            os.makedirs(dirPathInvalid,exist_ok=True)
            
            if ((statusTrain and statusTest) and statusNumericalColoumns) and statusDataDrift:

                trainDataFram.to_csv(
                    self.dataValidationConfig.valid_train_file_path,index=False,header=True
                )

                testDataFrame.to_csv(
                    self.dataValidationConfig.valid_test_file_path,index=False,header=True
                )
            else:
                trainDataFram.to_csv(
                    self.dataValidationConfig.invalid_train_file_path,index=False,header=True
                )

                testDataFrame.to_csv(
                    self.dataValidationConfig.invalid_test_file_path,index=False,header=True
                )

            dataValidationArtifact = DataValidationArtifact(
                validation_status = ((statusTrain and statusTest) and statusNumericalColoumns) and statusDataDrift,
                valid_train_file_path = self.dataValidationConfig.valid_train_file_path,
                valid_test_file_path = self.dataValidationConfig.valid_test_file_path,
                invalid_train_file_path = self.dataValidationConfig.invalid_train_file_path,
                invalid_test_file_path = self.dataValidationConfig.invalid_test_file_path,
                drift_report_file_path = self.dataValidationConfig.drift_report_file_path,
                sechema_validation_report_file_path = self.dataValidationConfig.drift_report_file_path
            
            )
            return dataValidationArtifact


        except Exception as e:
            raise NetworkSecurityException(e,sys)



