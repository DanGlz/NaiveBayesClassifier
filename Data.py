import pandas as pd
import os
import re


class data:
    _structureDict = {}
    _train_df = None

    def __init__(self, path, bins):
        self.bins = bins
        self.path = path
        self.getStructure()
        # self.printDict();

    # Add Structure to dictionary
    def getStructure(self):
        lines = tuple(open(self.path + "/Structure.txt", 'r'))
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
        self._train_df = pd.read_csv(self.path + "/train.csv")
        self.fillMissingValues()
        self.discretization(self._train_df)
        cs=classifier(self._train_df,self._structureDict,self.bins)
        cs.preparedata()
        self._train_df.to_csv("trainresults1.csv")

    def fillMissingValues(self):
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


    def discretization(self, df):
        for column in df.columns:
            if self._structureDict[column] == "NUMERIC":
                minval = df[column].min()
                maxval = df[column].max()
                weight = float(maxval - minval) / float(self.bins)
                cutpoints = []
                labels = []
                cutpoints.append(float("-inf"))
                for i in range(self.bins):
                    cutpoints.append(minval + i * weight)
                cutpoints.append(float("inf"))
                for j in range(self.bins+1):
                    labels.append(j + 1)
                df[column] = pd.cut(df[column], bins=cutpoints, labels=labels, include_lowest=True)
class classifier:
    attributecountdict={}
    classcountdict={}
    def __init__(self,df,struct,bins):
        self.df=df
        self.struct=struct
        self.bins=bins
    def preparedata(self):
        for key in self.struct:
            if self.struct[key]=="NUMERIC":
                self.attributecountdict[key] =self.bins
            else:
                count=len(self.struct[key])
                self.attributecountdict[key] = count
        self.classcountdict=self.df["class"].value_counts()
    def classify(self,testset):
        m=2






####main####
Data = data(os.path.dirname(os.path.realpath(__file__)),3)
Data.loadTrainDataFrame()

