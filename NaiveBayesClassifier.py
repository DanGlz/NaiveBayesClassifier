import pandas as pd
import re


class data:
    _structureDict = {}
    _train_df = None
    _classifier=None

    def __init__(self, path, bins):
        self.bins = bins
        self.path = path
        self.getStructure()

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
        self._classifier=classifier(self._train_df,self._structureDict,self.bins)
        self._classifier.preparedata()
    def loadTestSet(self):

        dftest=pd.read_csv(self.path + "/test.csv")
        self.discretization(dftest)
        test_result=self._classifier.classify(dftest)
        text_file = open(self.path+"/output.txt", "w")
        text_file.write(test_result)
        text_file.close()

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
                for i in range(self.bins-1):
                    cutpoints.append(minval + i * weight)
                cutpoints.append(float("inf"))
                for j in range(self.bins):
                    labels.append(j + 1)
                df[column] = pd.cut(df[column], bins=cutpoints, labels=labels, include_lowest=True)
                print (df[column].value_counts())
            else:
                check = "true"
                for val in self._structureDict[column]:
                    if val.isdigit():
                        check="false"
                        break
                if check == "true":
                    df[column]=df[column].str.lower()

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
        countclass=self.df["class"].value_counts().to_dict()
        for key in countclass:
            self.classcountdict[str(key)]=countclass[key]


    def classify(self,testset):
        #initialization of variables
        classification_testfile=""
        m=2
        count_no=0
        count_yes=0
        count_correct=0
        num_of_row_in_train = self.df.shape[0]
        matching_class_atribute_dict ={}
        #go over each row and classify using naive bayes
        for index, row in testset.iterrows():
            mestimate={}
            #initialize mestiamte for each class value
            for cls in self.struct["class"]:
                mestimate[str(cls)] = 1
            for colname in self.df.columns:
                if colname =="class":
                    continue
                for cls in self.struct["class"]:
                    cls=str(cls)
                    # memoization of all attribute value and class value that match
                    dictKey =colname+"_"+str(row[colname])+"_"+str(cls)
                    if dictKey in matching_class_atribute_dict:
                        samples_with_both_values = matching_class_atribute_dict[dictKey]
                    else:
                        real_cls=cls
                        if cls.isdigit():
                            real_cls=int(real_cls)
                        samples_with_both_values = len(self.df.loc[(self.df[colname] == row[colname]) & (self.df["class"] == real_cls)])
                        matching_class_atribute_dict[dictKey] = samples_with_both_values
                    num_of_diff_values_attr = self.attributecountdict[colname]
                    num_of_vals_class=self.classcountdict[cls]
                    mestimate[cls] = float(mestimate[cls])*(samples_with_both_values+(m/num_of_diff_values_attr))/( num_of_vals_class+m)
            for cls in self.struct["class"]:
                cls=str(cls)
                mestimate[str(cls)]=float(mestimate[cls])*(float(self.classcountdict[cls])/num_of_row_in_train)
            #choose best matching class by mestimate
            classification = max(mestimate.iterkeys(), key=(lambda key: mestimate[key]))
            classification_testfile= classification_testfile+str(index+1)+" "+str(classification)+"\n"

            ##delete all from here
            if(classification == row["class"]):
             count_correct=count_correct+1
            if classification=="yes":
             count_yes=count_yes+1
            else:
                count_no=count_no+1;

        print("yes")
        print(count_yes)
        print("no")
        print(count_no)
        print ("correct percentage:")
        print (count_correct)

        return classification_testfile

