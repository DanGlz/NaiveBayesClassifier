from tkinter import *
from tkinter import filedialog as fd
import pandas as pd
import NaiveBayesClassifier
import tkinter.messagebox
import os.path

class GUI:

    _nbc = None

    def __init__(self, myroot):
        self.test_df=None;
        self.train_df = None;
        self.bins = 0
        self.BuildPassed = False;
        self.root = myroot
        root.title("Naive Bayes Classifier")
        # define labels, entry`s and c #
        self.Path_Label = Label(root, text='Directory Path')   # path
        self.Path_Entry = Entry(root, width=60)
        self.Path_Browse_button = Button(root, text="Browse", command=self.browseClick, width=14)
        self.Bins_Labels = Label(root, text='Discretization Bins')  # Bins
        self.Bins_Entry = Entry(root, width=20)
        self.Bins_Entry.configure(state='disabled')
        self.Build_button = Button(root, text="Build", command=self.buildClick, width=25)   # Build and Classify
        self.Classify_button = Button(root, text="Classify", command=self.classifyClick, width=25)
        #  locate labels ,entry's and buttons on grid #
        self.Path_Label.grid(row=3, pady=35, padx=30)   # path
        self.Path_Entry.grid(row=3, column=1, padx=10, stick=W)
        self.Path_Browse_button.grid(row=3, column=2, padx=10)
        self.Bins_Labels.grid(row=4, column=0)    # Bins
        self.Bins_Entry.grid(row=4, column=1, padx=10, stick=W + N)
        self.Build_button.grid(row=5, column=1, pady=20)  # Build and Classify
        self.Classify_button.grid(row=6, column=1, pady=10)
        # set the size of the window
        self.root.geometry('{}x{}'.format(700, 350))
        self.root.resizable(0, 0)  # disable the option to resize the window

    #  handles the browse button
    def browseClick(self):
        path = fd.askdirectory(parent=root, title='Choose the directory path')
        self.Path_Entry.delete(0, END)
        self.Path_Entry.insert(0, path)
        if self.checkValidPath():
            self.Bins_Entry.configure(state='normal')
            self.train_df = pd.read_csv(str(self.Path_Entry) + "/train.csv")
        else:
            self.train_df = None
            self.Bins_Entry.configure(state='disabled')

    # handled the Build button
    def buildClick(self):
        if self.checkValidPath() and self.checkValidBins():
            self._nbc = NaiveBayesClassifier.data(str(self.Path_Entry), self.bins)
            self.BuildPassed = True
            tkinter.messagebox.showinfo("Message", "Building classifier using train-set is done!")
        else:
            self.BuildPassed = False
    # handled the Classify button
    def classifyClick(self):
        if not self.BuildPassed:
            tkinter.messagebox.showinfo("Error", "You need to build the model first!")
        else:
            self._nbc

  # Checks if all the files are exists in the given directory path
    def checkValidPath(self):
        error = False
        missing_files = ""
        if not os.path.isfile(self.Path_Entry.get()+"/Structure.txt"):
            error = True
            missing_files += "<Structure.txt> "
        if not os.path.isfile(self.Path_Entry.get() + "/train.csv"):
            error = True
            missing_files += "<train.csv> "
        if not os.path.isfile(self.Path_Entry.get() + "/test.csv"):
            error = True
            missing_files += "<test.csv> "
        if error:
            tkinter.messagebox.showinfo("Error", "The following files are missing in the directory: \n" + missing_files)
            return False
        return True

    # Checks if bins value is valid
    def checkValidBins(self):
        self.bins = self.Bins_Entry.get()
        num_of_records= self.train_df[0]
        # check if the bins value is digit AND bigger then 1
        if not self.bins.isdigit() or not int(self.bins) > 1:
            tkinter.messagebox.showinfo("Error", "The bins value is not valid. Bins value must be digit!")
            return False
        if int(self.bins) < 2 or int(self.bins) > num_of_records:
            tkinter.messagebox.showinfo("Error", "The bins value is out of range!")
            return False
        self.bins = int(self.bins)
        return True;

root = Tk()
NaveBayesClassifier_Gui = GUI(root)
root.mainloop()
