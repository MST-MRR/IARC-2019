'''
Python ver 2.7.15
This is a GUI for any tools that require one, such as the plotter that graphs
csv files and a config maker to customize graphs.
'''
import Tkinter as tk
import ttk

class PlotterGUI:
  def __init__(self, master):
    self.notebook = ttk.Notebook(master) #Makes tabs for the GUI
    self.notebook.grid(column=0, row=0) #TODO Switch to the grid system for organizing GUI elements

    #Contents of first tab
    #TODO Make the plotter for the first tab
    self.plotter_frame = ttk.Frame(master)
    self.plotter_label = ttk.Label(self.plotter_frame, text="WIP: Plotter functionality will be added soon")

    #Contents of second tab
    #TODO Make the config maker for the second tab
    self.config_mk_frame = ttk.Frame(master)
    self.config_mk_label = tk.Label(self.config_mk_frame, text="WIP: Config maker functionality will be added soon")

    #Organizing contents of first tab
    self.plotter_frame.grid(column=0, row=0)
    self.plotter_label.grid(column=0, row=0)

    #Organizing contents of second tab
    self.config_mk_frame.grid(column=0, row=0)
    self.config_mk_label.grid(column=0, row=0)

    #Creating the tabs themselves
    self.notebook.add(self.plotter_frame, text="Plotter")
    self.notebook.add(self.config_mk_frame, text="Config maker")

root = tk.Tk()
app = PlotterGUI(root) #Adds all GUI contents to the window

root.title("MST IARC Plotter and Config Maker")

#Sets the favicon at top-leftmost of the Tkinter GUI
icon_name = 'ninja_icon.gif'
icon_img = tk.PhotoImage(file='./tools/gui/' + icon_name)
root.tk.call('wm', 'iconphoto', root._w, icon_img)

root.mainloop()
#root.destroy() Explicit destroy call, needed in some conditions