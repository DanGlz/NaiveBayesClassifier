import pandas as pd
import re

# a class that manages all the dta and classification of the test and train set
class NaiveBayesClassifier:
    _structureDict = {}
    _train_df = None
    _classifier = None
    # constructor
    def __init__(self, path, bins):
        self.bins = bins
        self.path = path
        self.getStructure()
        self.minval={}
        self.maxval={}

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

    # loads the train set and prepares data for the classifier
    def load_train_data_frame(self):
        self._train_df = pd.read_csv(self.path + "/train.csv")
        self.fill_missing_values()
        self.get_max_min_vals_in_train()
        self.discretization(self._train_df)
        self._classifier = classifier(self._train_df,self._structureDict,self.bins)
        self._classifier.prepare_data()

    # loads the testset for the classifer
    def load_test_set(self):
        dftest = pd.read_csv(self.path + "/test.csv")
        self.discretization(dftest)
        test_result = self._classifier.classify(dftest)
        text_file = open(self.path+"/output.txt", "w")
        text_file.write(test_result)
        text_file.close()

    # fills the missingvalues by average or most common( mode)
    def fill_missing_values(self):
        for columnName in self._train_df.columns:
            if columnName == "class":
                continue
            if self._structureDict[columnName] == "NUMERIC":
                self._train_df[columnName].fillna(self._train_df[columnName].mean(), inplace=True)
            else:
                self._train_df[columnName].fillna(self._train_df[columnName].mode()[0], inplace=True)

    # creates a two dicts that hold the max value and min value of each column in the test set
    def get_max_min_vals_in_train(self):
        for column in self._train_df.columns:
            self.minval[column] = self._train_df[column].min()
            self.maxval[column] = self._train_df[column].max()

    # turns numeric values to categorial
    def discretization(self, df):
        for column in df.columns:
            if self._structureDict[column] == "NUMERIC":
                minval = self.minval[column]
                maxval = self.maxval[column]
                weight = float(maxval - minval) / float(self.bins)
                cutpoints = []
                labels = []
                # create cut points for binning
                cutpoints.append(float("-inf"))
                for i in range(self.bins-1):
                    cutpoints.append(minval + i * weight)
                cutpoints.append(float("inf"))
                for j in range(self.bins):
                    labels.append(j + 1)
                df[column] = pd.cut(df[column], bins=cutpoints, labels=labels, include_lowest=True)
            else:
                # if not numeric so turn all values to lower case
                check = "true"
                for val in self._structureDict[column]:
                    if val.isdigit():
                        check = "false"
                        break
                if check == "true":
                    df[column] =df[column].str.lower()

# class that handels all the classification of the test set
class classifier:
    attributecountdict={}
    classcountdict={}

    # constructor
    def __init__(self,df,struct,bins):
        self.df=df
        self.struct=struct
        self.bins=bins

    # prepare the data for the classifer according to the info given by the train set
    def prepare_data(self):
        for key in self.struct:
            if self.struct[key] == "NUMERIC":
                self.attributecountdict[key] = self.bins
            else:
                self.attributecountdict[key] = len(self.struct[key])
        countclass=self.df["class"].value_counts().to_dict()
        for key in countclass:
            self.classcountdict[str(key)] = countclass[key]

    # returns a string that contains the classification for the given testset
    def classify(self,testset):
        # initialization of variables
        classification_testfile=""
        m=2
        count_no=0
        count_yes=0
        count_correct=0
        num_of_row_in_train = self.df.shape[0]
        matching_class_atribute_dict ={}
        # go over each row and classify using naive bayes
        for index, row in testset.iterrows():
            mestimate={}
            # initialize mestiamte for each class value
            for cls in self.struct["class"]:
                mestimate[str(cls)] = 1
            for colname in self.df.columns:
                if colname == "class":
                    continue
                for cls in self.struct["class"]:
                    cls = str(cls)
                    # memoization of all attribute value and class value that match
                    dictKey = colname + "_" + str(row[colname]) + "_" + str(cls)
                    if dictKey in matching_class_atribute_dict:
                        samples_with_both_values = matching_class_atribute_dict[dictKey]
                    else:
                        real_cls = cls
                        if cls.isdigit():
                            real_cls = int(real_cls)
                        samples_with_both_values = len(self.df.loc[(self.df[colname] == row[colname]) & (self.df["class"] == real_cls)])
                        matching_class_atribute_dict[dictKey] = samples_with_both_values
                    num_of_diff_values_attr = self.attributecountdict[colname]
                    num_of_vals_class = self.classcountdict[cls]
                    mestimate[cls] = float(mestimate[cls])*(samples_with_both_values+(m/num_of_diff_values_attr))/( num_of_vals_class+m)
            for cls in self.struct["class"]:
                cls = str(cls)
                mestimate[str(cls)] = float(mestimate[cls])*(float(self.classcountdict[cls])/num_of_row_in_train)
            # choose best matching class by mestimate
            classification = max(mestimate.iterkeys(), key=(lambda key: mestimate[key]))
            classification_testfile = classification_testfile+str(index+1)+" "+str(classification)+"\n"
        return classification_testfile