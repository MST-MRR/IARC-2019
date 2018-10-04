
from tkinter import *
from tkinter import ttk
import csv

def updateSettings():
    #using the csv for the GUI
    Status_airSpeed = Update(check_air_speed)
    Status_altitude = Update(check_altitude)
    Status_pitch = Update(check_pitch)
    Status_roll = Update(check_roll)
    Status_yaw = Update(check_yaw)
    Status_xVelocity = Update(check_xVelocity)
    Status_yVelocity = Update(check_yVelocity)
    Status_zVelocity = Update(check_zVelocity)
    Status_voltage = Update(check_voltage)
    filename = "C:/Users/jonat/Desktop/GUI_Settings.csv"
    with open(filename, 'r') as g:
        reader = csv.reader(g)
        GUI_Settings_List = list(reader)
    Status_List = [Status_airSpeed,Status_altitude,Status_pitch,Status_roll,Status_yaw,Status_xVelocity,Status_yVelocity,Status_zVelocity,Status_voltage]
    for i in GUI_Settings_List:
        GUI_Settings_List[i+2] = Status_List[i]
        

#Defining the properties for the window
window = Tk()
window.title("Multirotor Robot Data Graphing Tool")
window.geometry('750x500')

#creating the seperate tabs for live/not live
tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1,text='Live Graphing Settings')
tab_control.add(tab2,text='After-The-Fact Graphing Settings')

#defining what hte update button does
def Update(variableName):
    if(variableName.get()):
        return True
    else:
        return False

#defining a single graph section for tab 1
name = "Graph1"
grph_lbl= Label(tab1,text=name,font=("Arial Bold", 15))#grpah label
grph_lbl.grid(column=0,row=0)
update_grph_btn= Button(tab1,text="Click to Update Section",command=updateSettings)#Button to update
update_grph_btn.grid(column=1, row=0)

#The variables to read if each are checked or not
check_air_speed = BooleanVar()
check_altitude = BooleanVar()
check_pitch = BooleanVar()
check_roll = BooleanVar()
check_yaw = BooleanVar()
check_xVelocity = BooleanVar()
check_yVelocity = BooleanVar()
check_zVelocity = BooleanVar()
check_voltage = BooleanVar()

#All the check mark Buttons
air_speed_chk= Checkbutton(tab1,text="Air Speed",var=check_air_speed)
air_speed_chk.grid(column=0, row=1)
altitude_chk= Checkbutton(tab1,text="Altitude",var=check_altitude)
altitude_chk.grid(column=1, row=1)
pitch_chk= Checkbutton(tab1,text="Pitch",var=check_pitch)
pitch_chk.grid(column=2, row=1)
roll_chk= Checkbutton(tab1,text="Roll",var=check_roll)
roll_chk.grid(column=3, row=1)
yaw_chk= Checkbutton(tab1,text="Yaw",var=check_yaw)
yaw_chk.grid(column=4, row=1)
xVelocity_chk= Checkbutton(tab1,text="xVelocity",var=check_xVelocity)
xVelocity_chk.grid(column=5, row=1)
yVelocity_chk= Checkbutton(tab1,text="yVelocity",var=check_yVelocity)
yVelocity_chk.grid(column=6, row=1)
zVelocity_chk= Checkbutton(tab1,text="zVelocity",var=check_zVelocity)
zVelocity_chk.grid(column=7, row=1)
voltage_chk= Checkbutton(tab1,text="Voltage",var=check_voltage)
voltage_chk.grid(column=8, row=1)


tab_control.pack(expand=1, fill='both')#should be near the end?
window.mainloop()#this needs to be at the end