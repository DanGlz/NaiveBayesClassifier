from tkinter import *
from tkinter import filedialog as fd
import tkinter.messagebox
import os.path

class GUI:
    def __init__(self, myroot):
        self.root = myroot
        root.title("Naive Bayes Classifier")
        # define labels, entry`s and buttons #
        # path:
        self.Path_Label = Label(root, text='Directory Path')
        self.Path_Entry = Entry(root, width=60)
        self.Path_Browse_button = Button(root, text="Browse", command=self.browseClick, width=14)
        # Bins:
        self.Bins_Labels = Label(root, text='Discretization Bins')
        self.Bins_Entry = Entry(root, width=20)
        # Build and Classify
        self.Build_button = Button(root, text="Build", command=self.buildClick, width=25)
        self.Classify_button = Button(root, text="Classify", command=self.classifyClick, width=25)
        #  set labels and entry's on grid #
        # path:
        self.Path_Label.grid(row=3, pady=35, padx=30)
        self.Path_Entry.grid(row=3, column=1, padx=10, stick=W)
        self.Path_Browse_button.grid(row=3, column=2, padx=10)
        # Bins:
        self.Bins_Labels.grid(row=4, column=0)
        self.Bins_Entry.grid(row=4, column=1, padx=10, stick=W + N)
        # Build and Classify
        self.Build_button.grid(row=5, column=1, pady=20)
        self.Classify_button.grid(row=6, column=1, pady=10)
        # set the size of the window
        self.root.geometry('{}x{}'.format(700, 350))
        self.root.resizable(0, 0)  # disable the option to resize the window

    def browseClick(self):
        path = fd.askdirectory(parent=root, title='Choose the directory path')
        self.Path_Entry.delete(0, END)
        self.Path_Entry.insert(0, path)

    def buildClick(self):
        if self.checkValidPath() and self.checkValidBins():
            tkinter.messagebox.showinfo("Passed")

    def classifyClick(args):
        pass
  # Check if all the files are exists in the given directory path
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

    def checkValidBins(self):
        bins = self.Bins_Entry.get()
        # check if the bins value is digit AND bigger then 1
        if not bins.isdigit() or not int(bins) > 1:
            tkinter.messagebox.showinfo("Error", "The bins value is not valid!")
            return False
        return True
root = Tk()
NaveBayesClassifier_Gui = GUI(root)
root.mainloop()
