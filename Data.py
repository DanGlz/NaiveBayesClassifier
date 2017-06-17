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
        dftest=pd.read_csv(self.path + "/test.csv")
        self.discretization(dftest)
        cs.classify(dftest)
        self._train_df.to_csv("trainresults1.csv")

    def fillMissingValues(self):
        for columnName in self._train_df.columns:
            if columnName == "class":
                continue
            if self._structureDict[columnName] == "NUMERIC":
                self._train_df[columnName].fillna(self._train_df[columnName].mean(), inplace=True)
            else:
                self._train_df[columnName].fillna(self._train_df[columnName].mode()[0], inplace=True)

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
                self.attributecountdict[key] = self.bins
            else:
                count=len(self.struct[key])
                self.attributecountdict[key] = count
        self.classcountdict=self.df["class"].value_counts()

    def classify(self,testset):
        print("classify started")
        m=2
        count_no=0
        count_yes=0
        for index, row in testset.iterrows():
            mestimate={}
            for cls in self.struct["class"]:
                mestimate[cls] = 1
            for colname in self.df.columns:
                if colname =="class":
                      continue;
                for cls in self.struct["class"]:
                    samples_with_both_values = len(self.df.loc[(self.df[colname] == row[colname]) & (self.df["class"] == cls)])
                    num_of_diff_values_attr = self.attributecountdict[colname]
                    num_of_vals_class=self.classcountdict[cls]
                  #  print(float(mestimate[cls])*(samples_with_both_values+(m/num_of_diff_values_attr))/( num_of_vals_class+m))
                    mestimate[cls] = float(mestimate[cls])*(samples_with_both_values+(m/num_of_diff_values_attr))/( num_of_vals_class+m)
            for cls in self.struct["class"]:
                mestimate[cls]=float(mestimate[cls])*(float(self.classcountdict[cls])/self.df.shape[0])
            classification = max(mestimate.iterkeys(), key=(lambda key: mestimate[key]))
            if classification=="yes":
                print("yes")
                count_yes=count_yes+1
            else:
                print("no")
                count_no=count_no+1;

        print("yes")
        print(count_yes)
        print("no")
        print(count_no)







####main####
Data = data(os.path.dirname(os.path.realpath(__file__)),3)
Data.loadTrainDataFrame()

