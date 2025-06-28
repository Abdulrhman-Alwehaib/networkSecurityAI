from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trainingFilePath:str
    testFilePath:str