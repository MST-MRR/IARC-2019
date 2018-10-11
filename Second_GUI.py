
from tkinter import *
from tkinter import ttk
import csv

class GUI:
    settings_file = "GUI_Settings.csv"

    #defining what different commands do
    def Update(self, variable_name):
        return 1 if variable_name.get() else 0

    def ChangeName(self):
        self.grph_lbl.destroy()

        self.newName_box = Entry(self.tab1,width=20)
        self.newName_box.grid(column=0,row=0,columnspan=2)

        self.update_Name_btn.destroy()

        self.submit_btn = Button(self.tab1,text="Submit",command=self.RealChange)
        self.submit_btn.grid(column=2,row=0,columnspan=2)

    def RealChange(self):
        self.name = self.newName_box.get()

        self.newName_box.destroy()
        self.submit_btn.destroy()

        self.grph_lbl= Label(self.tab1,text=self.name,font=("Arial Bold", 15))#graph label
        self.grph_lbl.grid(column=0,row=0,columnspan=2)

        self.update_Name_btn = Button(self.tab1,text="Click to change Name",command=self.ChangeName)
        self.update_Name_btn.grid(column=2,row=0,columnspan=2)

    def updateSettings(self):
        #using the csv for the GUI

        StatusDict = {
            "Status_GraphName" : self.name,
            "Status_lowerTime" : self.lowerTime_chk.get(),
            "Status_upperTime" : self.upperTime_chk.get(),
            "Status_airSpeed" : self.Update(self.check_air_speed),
            "Status_altitude" : self.Update(self.check_altitude),
            "Status_pitch" : self.Update(self.check_pitch),
            "Status_roll" : self.Update(self.check_roll),
            "Status_yaw" : self.Update(self.check_yaw),
            "Status_xVelocity" : self.Update(self.check_xVelocity),
            "Status_yVelocity" : self.Update(self.check_yVelocity),
            "Status_zVelocity" : self.Update(self.check_zVelocity),
            "Status_voltage" : self.Update(self.check_voltage)
        }

        with open(GUI.settings_file, 'w') as g:
            for key, value in StatusDict.items():
                g.write("{} = {}\n".format(key, str(value)))
            
        #Status_List = [Status_lowerTime,Status_upperTime,Status_airSpeed,Status_altitude,Status_pitch,Status_roll,Status_yaw,Status_xVelocity,Status_yVelocity,Status_zVelocity,Status_voltage]

            
    def __init__(self):
        #Defining the properties for the window

        #
        # Window setup
        window = Tk()
        window.title("Multirotor Robot Data Graphing Tool")
        window.geometry('750x500')

        #creating the seperate tabs for live/not live

        #
        # Separate tabs
        tab_control = ttk.Notebook(window)

        self.tab1 = ttk.Frame(tab_control)
        self.tab2 = ttk.Frame(tab_control)
        tab_control.add(self.tab1, text='Live Graphing Settings')
        tab_control.add(self.tab2, text='After-The-Fact Graphing Settings')

        #defining a single graph section for tab 1

        #
        # Per graph implementation

        # Header - Graph name
        self.name = "Graph1"
        self.grph_lbl= Label(self.tab1,text=self.name,font=("Arial Bold", 15))#graph label
        self.grph_lbl.grid(column=0,row=0,columnspan=2)

        # Update header
        self.update_Name_btn = Button(self.tab1,text="Click to change Name",command=self.ChangeName)
        self.update_Name_btn.grid(column=2,row=0,columnspan=2)

        # Update config
        update_grph_btn= Button(self.tab1,text="Click to Update Section",command=self.updateSettings)#Button to update
        update_grph_btn.grid(column=4,row=0,columnspan=2)

        #The variables to read if each are checked or not
        self.check_air_speed = BooleanVar()
        self.check_altitude = BooleanVar()
        self.check_pitch = BooleanVar()
        self.check_roll = BooleanVar()
        self.check_yaw = BooleanVar()
        self.check_xVelocity = BooleanVar()
        self.check_yVelocity = BooleanVar()
        self.check_zVelocity = BooleanVar()
        self.check_voltage = BooleanVar()

        #All the check mark Buttons

        #
        # Setup check mark buttons

        # Each requires tab, text, variable, grid x & y
        self.air_speed_chk= Checkbutton(self.tab1,text="Air Speed",var=self.check_air_speed)
        self.air_speed_chk.grid(column=0, row=1)

        self.altitude_chk= Checkbutton(self.tab1,text="Altitude",var=self.check_altitude)
        self.altitude_chk.grid(column=1, row=1)

        self.pitch_chk= Checkbutton(self.tab1,text="Pitch",var=self.check_pitch)
        self.pitch_chk.grid(column=2, row=1)

        self.roll_chk= Checkbutton(self.tab1,text="Roll",var=self.check_roll)
        self.roll_chk.grid(column=3, row=1)

        self.yaw_chk= Checkbutton(self.tab1,text="Yaw",var=self.check_yaw)
        self.yaw_chk.grid(column=4, row=1)

        self.xVelocity_chk= Checkbutton(self.tab1,text="xVelocity",var=self.check_xVelocity)
        self.xVelocity_chk.grid(column=5, row=1)

        self.yVelocity_chk= Checkbutton(self.tab1,text="yVelocity",var=self.check_yVelocity)
        self.yVelocity_chk.grid(column=6, row=1)

        self.zVelocity_chk= Checkbutton(self.tab1,text="zVelocity",var=self.check_zVelocity)
        self.zVelocity_chk.grid(column=7, row=1)

        self.voltage_chk= Checkbutton(self.tab1,text="Voltage",var=self.check_voltage)
        self.voltage_chk.grid(column=8, row=1)

        #
        # Time interval settings
        self.lowerTime_lbl= Label(self.tab1, text="Time interval(seconds) Lower:")
        self.lowerTime_lbl.grid(column=0, row=2,columnspan=2)

        self.lowerTime_chk= Entry(self.tab1,width=5)
        self.lowerTime_chk.grid(column=2, row=2)

        self.upperTime_lbl= Label(self.tab1, text="Upper:")
        self.upperTime_lbl.grid(column=3, row=2)

        self.upperTime_chk= Entry(self.tab1,width=5)
        self.upperTime_chk.grid(column=4, row=2)

        #
        # Display window
        tab_control.pack(expand=1, fill='both')#should be near the end?
        window.mainloop()#this needs to be at the end


if __name__ == "__main__":
    myClass = GUI()
