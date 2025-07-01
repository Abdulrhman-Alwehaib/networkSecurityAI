#configuration details
from datetime import datetime
import os
from networksecurity.constant import training_pipline

print(training_pipline.PIPLINE_NAME)
print(training_pipline.ARTIFACT_DIR)

#General purpose class
class TrainingPiplineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipline_name = training_pipline.PIPLINE_NAME

        self.artifact_name = training_pipline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name,timestamp)

        self.timestamp:str = timestamp

class DataIngestionConfig:
    def __init__(self,training_pipline_config:TrainingPiplineConfig):
        self.data_ingestion_dir:str = os.path.join(
            training_pipline_config.artifact_dir,
            training_pipline.DATA_INGESTION_DIR_NAME
        )

        self.feature_store_file_path:str = os.path.join(
            self.data_ingestion_dir,training_pipline.DATA_INGESTION_FEATURE_STORE_DIR,training_pipline.FILE_NAME
        )

        self.training_file_path:str = os.path.join(
            self.data_ingestion_dir,training_pipline.DATA_INGESTION_INGESTRION_DIR,training_pipline.TRAIN_FILE_NAME
        )

        self.test_file_path:str = os.path.join(
            self.data_ingestion_dir,training_pipline.DATA_INGESTION_INGESTRION_DIR,training_pipline.TEST_FILE_NAME
        )


        self.train_test_split_ratio:float = training_pipline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name:str = training_pipline.DATA_INGESTION_COLLECTION_NAME
        self.database_name:str = training_pipline.DATA_INGESTION_DATABASE_NAME



class DATAVALIDATIONConfig:
    def __init__(self,training_pipline_config:TrainingPiplineConfig):
        self.data_validation_dir:str = os.path.join(training_pipline_config.artifact_dir,training_pipline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir:str = os.path.join(self.data_validation_dir,training_pipline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir:str = os.path.join(self.data_validation_dir,training_pipline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path:str = os.path.join(self.valid_data_dir,training_pipline.TRAIN_FILE_NAME)
        self.valid_test_file_path:str = os.path.join(self.valid_data_dir,training_pipline.TEST_FILE_NAME)
        self.invalid_train_file_path:str = os.path.join(self.invalid_data_dir,training_pipline.TRAIN_FILE_NAME)
        self.invalid_test_file_path:str = os.path.join(self.invalid_data_dir,training_pipline.TEST_FILE_NAME)
        self.drift_report_file_path:str = os.path.join(
            self.data_validation_dir,
            training_pipline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
        )
        self.schema_validation_file_path:str = os.path.join(
            self.data_validation_dir,
            training_pipline.DATA_VALIDATION_SCHEMA_FILE_NAME
            
        )



class DataTransformationConfig:
    def __init__(self,training_piplineConfig:TrainingPiplineConfig):
        self.dataTransformationDir = os.path.join(training_piplineConfig.artifact_dir,training_pipline.DATA_TRANSFORMATION_DIR_NAME)
        self.dataTransformationObj = os.path.join(self.dataTransformationDir,training_pipline.DATA_TRANSFORMATION_TRANSFORMATIONOBJ_FILE_NAME)
        self.DataTransformedTrainPath = os.path.join(self.dataTransformationDir,training_pipline.TRAIN_FILE_NAME.replace("csv","npy"))
        self.DataTransformedTestPath = os.path.join(self.dataTransformationDir,training_pipline.TEST_FILE_NAME.replace("csv","npy"))
        
