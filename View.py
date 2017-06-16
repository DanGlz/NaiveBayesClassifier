from tkinter import *


def browseClick(args):
    pass


def buildClick(args):
    pass


def classifyClick(args):
    pass


class GUI:
    def __init__(self, myroot):
        self.root = myroot
        root.title("Naive Bayes Classifier")
        # define labels and entry`s and buttons
        # path:
        self.Path_Label = Label(root, text='Directory Path')
        self.Path_Entry = Entry(root, width=60)
        self.Path_Browse_button = Button(root, text="Browse", command=browseClick, width= 14)
        # Bins:
        self.Bins_Labels = Label(root, text='Discretization Bins')
        self.Bins_Entry=Entry(root, width=20)
        # Build and Classify
        self.Build_button = Button(root, text="Build", command=buildClick, width = 25)
        self.Classify_button = Button(root, text="Classify", command=classifyClick,width = 25)
        #  set labels and entry's on grid
        # path:
        self.Path_Label.grid(row=3,pady=35, padx=30)
        self.Path_Entry.grid(row=3, column=1, padx=10,stick=W)
        self.Path_Browse_button.grid(row=3, column=2, padx=10)
        # Bins:
        self.Bins_Labels.grid(row=4,column=0 )
        self.Bins_Entry.grid(row=4, column=1, padx=10, stick=W+N)
        # Build and Classify
        self.Build_button.grid(row=5,column=1,pady=20)
        self.Classify_button.grid(row=6,column=1,pady=10)
        # set the size of the window
        self.root.grid_rowconfigure(10)
        self.root.grid_columnconfigure(10)
        self.root.geometry('{}x{}'.format(700, 350))
        self.root.resizable(0,0)

      #  self.close_button = Button(root, text="Close", command=root.quit)
     #  self.close_button.pack()



root = Tk()
my_gui = GUI(root)
root.mainloop()