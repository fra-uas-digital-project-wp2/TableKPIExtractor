import os
import logging
import json
import csv 

from logging.handlers import RotatingFileHandler

try:
        path = globals()['_dh'][0]
except KeyError:
        path = os.path.dirname(os.path.realpath(__file__))
print(path)
SRC_DIR = os.path.join(path, "20240114_Expected_Values")
#OUT_DIR = os.path.join(path, "Expected_Values_Appended")
RAW_DIR = os.path.join(path, "input2")

print(SRC_DIR)

NAME_DICT = {
             "Scope 1" : "Scope 1 / Direct total GHGs emissions",
             "Scope 2" : "Scope 2 Energy indirect total GHGs emissions",
             "Scope 3" : "Scope 3 Upstream Energy indirect total GHGs emissions",
             "Scope 2 Market" : "Scope 2 Market Energy indirect total GHGs emissions",
             "Scope 2 Location" : "Scope 2 Location Energy indirect total GHGs emissions"
            }

def create_logger():
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)


    # Create a RotatingFileHandler with a max file size of 1MB and a maximum of 5 backup files
    file_handler = RotatingFileHandler('append.log', maxBytes=1024*1024, backupCount=5,encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)
    return logger

def load(file):
    full_path = os.path.join(SRC_DIR,file)
    print(f"File :'{full_path}' loading!")
    f = open(full_path)
    return json.load(f)

def save(file,data):
    full_path = os.path.join(OUT_DIR,file)
    print(f"File :'{full_path}' saving!")
    with open(full_path, 'w') as file:
        json.dump(data, file, indent=2)

     

def main():
    logger = create_logger()
    for file in os.listdir(SRC_DIR):
        
        #try:
        data = load(file)
        data["Scope 2 Market"] = {}
        data["Scope 2 Market"]["Year"] = []
        data["Scope 2 Market"]["Value"] = []
        data["Scope 2 Market"]["Page"] = []
        data["Scope 2 Market"]["ID"] = 9
        data["Scope 2 Location"] = {}
        data["Scope 2 Location"]["Year"] = []
        data["Scope 2 Location"]["Value"] = []
        data["Scope 2 Location"]["Page"] = []
        data["Scope 2 Location"]["ID"] = 10
 
        save(file,data)

        #except Exception as e:
           
        #    logger.error(f"File '{file}' had exception '{e}' ")


if __name__ == "__main__":
    main()