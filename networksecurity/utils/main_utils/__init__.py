import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os
import sys
import numpy as np
import pickle
import pandas as pd

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

def saveNumpyArray(FilePAth,array:np.array):
    try:
        dirPath = os.path.dirname(FilePAth)
        os.makedirs(dirPath,exist_ok=True)
        with open(FilePAth,"wb") as fileObj:
            np.save(fileObj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def SaveObjectAsPickleFile(filePath,obj:object):
    try:
        os.makedirs(os.path.dirname(filePath),exist_ok=True)
        with open(filePath,"wb") as fileObj:
            pickle.dump(obj,fileObj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

def readData(filePath)->pd.DataFrame:
        try:
            return pd.read_csv(filePath)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
