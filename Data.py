import pandas as pd
import os
import re
from scipy.stats import mode

class data:
    _structureDict = {}
    _train_df = None

    def __init__(self, path):
        self.path = path
        self.getStructure()
      # self.printDict();

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
        self._train_df = pd.read_csv(self.path+"/train.csv")
        self.fillMissingValues()

    def fillMissingValues (self):
        print("The null valus:")
        print(self._train_df.apply(lambda x: sum(x.isnull()), axis=0))
        for columnName in self._train_df.columns:
            if columnName == "class":
                continue
            if self._structureDict[columnName] == "NUMERIC":
                self._train_df[columnName].fillna(self._train_df[columnName].mean(), inplace=True)
            else:
                self._train_df[columnName].fillna(self._train_df[columnName].mode()[0], inplace=True)
        print("The null valus:")
        print(self._train_df.apply(lambda x: sum(x.isnull()), axis=0))
        self._train_df.to_csv("trainresults.csv")

####main####
Data = data(os.path.dirname(os.path.realpath(__file__)))
Data.loadTrainDataFrame("train")

