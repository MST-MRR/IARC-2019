
from tkinter import *
from tkinter import ttk
import csv


class GraphSettings:
    def __init__(self, tab):
        self.tab = tab

        # Header - Graph name
        self.name = "Graph1"
        self.grph_lbl = Label(self.tab, text=self.name, font=("Arial Bold", 15))  # graph label
        self.grph_lbl.grid(column=0, row=0, columnspan=2)

        # Update header
        self.update_Name_btn = Button(self.tab, text="Click to change Name", command=self.ChangeName)
        self.update_Name_btn.grid(column=2, row=0, columnspan=2)

        #
        # Setup check mark buttons
        self.check_boxes = []
        self.check_box_values = {}

        self.generate_check_boxes(self.tab, 1)

        #
        # Time interval settings
        self.lowerTime_lbl = Label(self.tab, text="Time interval(seconds) Lower:")
        self.lowerTime_lbl.grid(column=0, row=2, columnspan=2)

        self.lowerTime_chk = Entry(self.tab, width=5)
        self.lowerTime_chk.grid(column=2, row=2)

        self.upperTime_lbl = Label(self.tab, text="Upper:")
        self.upperTime_lbl.grid(column=3, row=2)

        self.upperTime_chk = Entry(self.tab, width=5)
        self.upperTime_chk.grid(column=4, row=2)

        update_grph_btn = Button(self.tab, text="Click to Update Section",
                                 command=self.updateSettings)  # Button to update
        update_grph_btn.grid(column=4, row=0, columnspan=2)

    def updateSettings(self):
        # using the csv for the GUI

        StatusDict = {"Status_GraphName": self.name, "Status_lowerTime": self.lowerTime_chk.get(),
                      "Status_upperTime": self.upperTime_chk.get()}

        StatusDict.update({"Status_{}".format(key): 1 if value.get() else 0 for key, value in self.check_box_values.items()})

        with open(GUI.settings_file, 'w') as g:
            for key, value in StatusDict.items():
                g.write("{} = {}\n".format(key, str(value)))

    def generate_check_boxes(self, tab, row):
        check_box_settings = ["Air Speed", "Altitude", "Pitch", "Roll", "Yaw", "xVelocity", "yVelocity", "zVelocity",
                              "Voltage"]

        i = 0

        # Chose this format because I don't think we will ever care about individual checkboxes values, only quick
        # iteration through the list to save
        for key in check_box_settings:
            self.check_box_values.update({key: BooleanVar()})
            self.check_boxes.append(Checkbutton(tab, text=key, var=self.check_box_values[key]))

            self.check_boxes[-1].grid(column=i, row=row)
            i += 1

    def ChangeName(self):
        self.grph_lbl.destroy()

        self.newName_box = Entry(self.tab, width=20)
        self.newName_box.grid(column=0, row=0, columnspan=2)

        self.update_Name_btn.destroy()

        self.submit_btn = Button(self.tab, text="Submit", command=self.RealChange)
        self.submit_btn.grid(column=2, row=0, columnspan=2)

    def RealChange(self):
        self.name = self.newName_box.get()

        self.newName_box.destroy()
        self.submit_btn.destroy()

        self.grph_lbl= Label(self.tab, text=self.name, font=("Arial Bold", 15))#graph label
        self.grph_lbl.grid(column=0, row=0, columnspan=2)

        self.update_Name_btn = Button(self.tab, text="Click to change Name", command=self.ChangeName)
        self.update_Name_btn.grid(column=2, row=0, columnspan=2)


class GUI:
    settings_file = "GUI_Settings.csv"

    def __init__(self):
        #
        # Window setup
        window = Tk()
        window.title("Multirotor Robot Data Graphing Tool")
        window.geometry('750x500')

        #
        # Separate tabs
        tab_control = ttk.Notebook(window)

        self.tab1 = ttk.Frame(tab_control)
        self.tab2 = ttk.Frame(tab_control)
        tab_control.add(self.tab1, text='Live Graphing Settings')
        tab_control.add(self.tab2, text='After-The-Fact Graphing Settings')

        #
        # Per graph implementation
        self.graphs = []
        self.graphs.append(GraphSettings(self.tab1))

        #
        # Display window
        tab_control.pack(expand=1, fill='both')#should be near the end?
        window.mainloop()#this needs to be at the end


if __name__ == "__main__":
    myClass = GUI()
