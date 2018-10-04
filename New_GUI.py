
from tkinter import *
from tkinter import ttk


#Definition of the Window
window = Tk()
window.title("Welcome to my first app!")
window.geometry('400x500')
class GUI:
    
    def __init__(self):
        
        print("hi")
        #Creates the tabs
        tab_control = ttk.Notebook(window)
        self.tab1 = ttk.Frame(tab_control)
        self.tab2 = ttk.Frame(tab_control)
        tab_control.add(self.tab1, text='Live Graphing Settings')
        tab_control.add(self.tab2, text='After-The-Fact Graphing Settings')

        #Defining a test function stuff
        self.i = 0
        self.checkIt = 0
        self.lbl = Label(self.tab1, text='Hello!')
        self.lbl.grid(column=0, row=1)

        tab_control.pack(expand=1, fill='both')
        my_graph = GUI()
        my_graph.newGraph()
        window.mainloop()

    def checkMarked(self):#this determines what to do if the button is or isnt checked
        if(self.checkIt):
            self.lbl.configure(text="It Was Checked!")
        else:
            self.lbl.configure(text="Hello!")
    
    def newGraph(self): #runs to make the section for a graph
        self.i = self.i + 1
        topSection = 5*(self.i-1)
        section = 5*(self.i-1) + 2
        vars()["var" + str(self.i)] = BooleanVar()
        #Top
        name = "Graph " + str(self.i)
        self.lbl = Label(self.tab1, text=name)
        self.lbl.grid(column=0, row=topSection)
        btn = Button(self.tab1, text="Click to update selection", command=self.checkMarked)
        btn.grid(column=1, row=topSection)
        #adding the headers to pick from to graph
        vars()["chk"+str(self.i)] = Checkbutton(self.tab1, text='Choose',var=vars()["var"+str(self.i)])
        vars()["chk"+str(self.i)].grid(column=0, row=(section+1))
        vars()["var"+str(self.i)] = self.checkIt

