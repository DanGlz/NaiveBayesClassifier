import pandas as pd
import os
import re

class data:
    _structureDict={};

    def __init__(self, path,bins):
        self.bins=bins
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

    def loadTrainDataFrame(self, filename):
        df= pd.read_csv(self.path+"/"+filename+".csv")
        self.fillMissingValues(df)

    def fillMissingValues (self, df):
        df =pd.read_csv(self.path+"/train.csv")  #delete before test!
        for columnName in df.columns:
            if self._structureDict[columnName] == "NUMERIC":
             df[columnName].fillna()

    def  discretion(self,df):
        for column in df.columns:
            if self._structureDict[column] == "NUMERIC":
                minval=column.min()
                maxval=column.max()
                weight= (minval+maxval)/self.bins
                cutpoints= []
                for i in range(1,self.bins):
                    cutpoints.append(minval+i*weight)
                labels=range(1,self.bins+1)
                df[column]=pd.cut(column, bins=cutpoints, labels=labels, include_lowest=True)




####main####

Data = data(os.path.dirname(os.path.realpath(__file__)))
Data.loadTrainDataFrame("train");

