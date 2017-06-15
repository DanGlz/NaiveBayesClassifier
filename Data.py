import pandas as pd
import os
import re

class data:
    _structureDict={};

    def __init__(self, path):
        self.path = path
        self.getStructure()
        self.printDict();
# Add Structure to dictionary
    def getStructure(self):
        lines = tuple(open(self.path+"/Structure.txt", 'r'))
        for line in lines:  # get line by line
            splitedLine = line.split()
            if splitedLine[2] == "NUMERIC":
                self._structureDict[splitedLine[1]] = "NUMERIC"  # add to dictionary
            else:
                splitedLine[2] = splitedLine[2].replace('{', '').replace('}', '')  # add to dictionary
                self._structureDict[splitedLine[1]] = re.split(',', splitedLine[2])

    def printDict(self):
        for keys, values in self._structureDict.items():
            print(keys)
            print(values)
            print(" ")

    def loadTrainDataFrame(self):
        df= pd.read_csv(self.path+"/train.csv")





Data = data(os.path.dirname(os.path.realpath(__file__)))


