from dataclasses import dataclass

#Later work
class ArtifactManager:
    @staticmethod
    def clean_invalid_data(path:str):
        pass
    @staticmethod
    def generate_report_summary(artifact):
        pass


@dataclass
class DataIngestionArtifact:
    trainingFilePath:str
    testFilePath:str

@dataclass
class DataValidationArtifact:
    validation_status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    drift_report_file_path:str
    ##
    ##feature work: schema validation report path
    ##
    sechema_validation_report_file_path:str


@dataclass
class DATATransformationArtifact:
    transformationObjectFilePAth:str
    transformedTrainFilePath:str
    transformedTestFilePath:str


