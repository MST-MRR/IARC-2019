'''
Python ver 2.7.15
This is a GUI for any tools that require one, such as the plotter that graphs
csv files and a config maker to customize graphs.

TODO Maaybe move description to the class
'''
import Tkinter as tk
import ttk
import tkFileDialog

#Importing the plotter backend. 
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__),"plotter"))
import plotter.plotter_backend as plotter_tool

class multiToolGUI:
  '''
  TODO Add explanation of class here
  '''
  def __init__(self):
    self.main_window = tk.Tk() #Creates the application window
    self.main_window.title("MST Multirotor Multitool")

    self.setIcon()

    self.notebook = ttk.Notebook(self.main_window) #Makes tabs for the GUI
    self.notebook.grid(columnspan=2, row=0)

    #Contents of first tab
    self.plotter_frame = ttk.Frame(self.main_window)
    self.plotter_label = ttk.Label(self.plotter_frame,
                                   text="Welcome to the IARC Plotter!")
    self.file_selector = ttk.Button(self.plotter_frame, text="Open .csv file",
                                    command=self.select_file)

    #Contents of second tab
    #TODO Make the config maker for the second tab
    self.config_mk_frame = ttk.Frame(self.main_window)
    self.config_mk_label = tk.Label(self.config_mk_frame,
                                    text="WIP: Reserved for second tool")

    #Positioning contents of first tab
    self.plotter_frame.grid(columnspan=2, row=0)
    self.plotter_label.grid(columnspan=2, row=0)
    self.file_selector.grid(columnspan=2, row=1)

    #Positioning contents of second tab
    self.config_mk_frame.grid(column=0, row=0)
    self.config_mk_label.grid(column=0, row=0)

    #Creating the tabs themselves
    self.notebook.add(self.plotter_frame, text="Plotter")
    self.notebook.add(self.config_mk_frame, text="Config maker")

    self.main_window.mainloop() #Starts the GUI event loop

    #TODO Figure out whether root.destroy() is needed and when it is needed
    #root.destroy() Explicit destroy call, needed in some conditions

  def select_file(self):
    '''
    Gets the filename and path of that file for the user chosen file.
    Then it creates GUI elements for the user to pick two column headers
    for the plotter to graph.
    '''
    self.csv_filename = tkFileDialog.askopenfilename(filetypes=[
                                                     ("CSV Files", "*.csv"),
                                                     ("All files","*.*")])
    if self.csv_filename:
      print(self.csv_filename)
      #Plotter backend code retrieves list of possible graph labels
      self.column_headers = plotter_tool.get_csv_headers(self.csv_filename)
      #Creates pull-down menus with graph label options and a submit button
      self.column_options_1 = ttk.Combobox(self.plotter_frame,
                                           values=self.column_headers)
      self.column_options_2 = ttk.Combobox(self.plotter_frame,
                                           values=self.column_headers)
      self.plotter_submit_button = ttk.Button(self.plotter_frame,
                                              text="Submit",
                                              command=self.submit_graph_options)

      #Widget positioning
      self.column_options_1.grid(column=0, row=2)
      self.column_options_2.grid(column=1, row=2)
      self.plotter_submit_button.grid(columnspan=2, row=3)

  def submit_graph_options(self):
    print('Submitted!')
    self.column_1_choice = self.column_options_1.get()
    self.column_2_choice = self.column_options_2.get()
    #Passes user chosen headers to backend code
    plotter_tool.submit_chosen_columns(self.csv_filename, self.column_1_choice,
                                       self.column_2_choice)

  def setIcon(self):
    '''
    Sets the favicon at top-leftmost of the Tkinter GUI
    '''
    try:
      self.icon_name = 'ninja_icon.gif'
      self.icon_path = os.path.join(os.path.dirname(__file__), self.icon_name)
      self.icon_img = tk.PhotoImage(file=self.icon_path)
      self.main_window.call('wm', 'iconphoto', self.main_window._w, 
                            self.icon_img)
      print("Ninja icon set successful, check the top-left part of the GUI!")
    except:
      print('Unable to set the awesome ninja icon for the application.')

if __name__ == '__main__':
  #Initializes the class and creates the application
  multiToolGUI()