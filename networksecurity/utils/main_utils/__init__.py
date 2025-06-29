import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os
import sys
import numpy as np
import dill
import pickle

#use with to close the file <dont delete it!>
def read_yaml_file(filePath:str)->dict:
    try:
        with open(filePath,"rb")as yamlFile:
            return yaml.safe_load(yamlFile)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def writeYampleFile(filePath,content,replace=False):
    try:
        if replace:
            if os.path.exists(filePath):
                os.remove(filePath)
        os.makedirs(os.path.dirname(filePath),exist_ok=True)
        with open(filePath, "a") as currentFile:
            yaml.dump(content,currentFile)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
