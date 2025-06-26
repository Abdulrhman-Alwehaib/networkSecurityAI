#find_packages will try to search for __init__.py in the current directory

from setuptools import find_packages,setup
from typing import List

def get_requirments()->List[str]:
    """
    this function will return list of requirments
    """
    requirments_list:List[str] = []
    try:
        with open("requirments.txt","r") as file:
            #Read lines from the file
            lines = file.readlines()
            #Proccess each line
            for line in lines:
                requirment = line.strip()
                #Ignore empty lines and -e.

                #-e . (short for --editable .) tells pip to install the current package in development mode 
                # (i.e., changes to code take effect immediately without reinstalling).

                if requirment and requirment != "-e .": #Ensures the line is not empty
                    requirments_list.append(requirment)
    except FileNotFoundError:
        print("requirments.txt file not found")
    
    return requirments_list

setup(
    name="Network Security AI",
    version="0.0.1",
    author="Abdulrhman",
    author_email="abdalrhmanmicro1@gmail.com",
    #will find folders that has __init__.py
    packages=find_packages(),
    install_requires = get_requirments()

)