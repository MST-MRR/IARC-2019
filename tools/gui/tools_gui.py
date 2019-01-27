'''
Python ver 2.7.15
This is a GUI for any tools that require one, such as the plotter that graphs
csv files and a config maker to customize graphs.

NOTE: There is a test file under tools/test/test_csv to test out the plotter.
'''
import Tkinter as tk
import ttk, tkFileDialog
#Importing the plotter backend. 
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__),"plotter"))
import plotter.plotter_backend as plotter_tool

class multiToolGUI:
  '''
  A class used to represent the GUI for the plotter (and future tools).

  Methods
  -------
  select_file()
    Gets the user chosen filename and filepath and creates widgets for the
    user to choose their graph labels in a drop-down menu
  submit_graph_options()
    Retrieves user-selected graph labels and plots a graph
  setIcon()
    Sets the GUI favicon
  '''

  def __init__(self):
    self.main_window = tk.Tk() #Creates the application window
    self.main_window.title("MST Multirotor Multitool")
    self.icon_name = 'ninja_icon.gif'
    self.setIcon(self.icon_name)

    self.notebook = ttk.Notebook(self.main_window) #Allows the creation of tabs
    self.notebook.grid(columnspan=2, row=0)

    #Positioning first tab widgets
    self.plotter_frame = ttk.Frame(self.main_window)
    self.plotter_label = ttk.Label(self.plotter_frame,
                                   text="Welcome to the Multirotor Plotter!")
    self.file_selector = ttk.Button(self.plotter_frame, text="Open .csv file",
                                    command=self.select_file)

    #Positioning contents of first tab
    self.plotter_frame.grid(columnspan=2, row=0)
    self.plotter_label.grid(columnspan=2, row=0)
    self.file_selector.grid(columnspan=2, row=1)

    #Creates the actual tab
    self.notebook.add(self.plotter_frame, text="Plotter")

    '''
    Second tab contents for future tool.
    #TODO Make the drone swarm controller simulator for the second tab
    self.tab_2_frame = ttk.Frame(self.main_window)
    self.tab_2_label = tk.Label(self.tab_2_frame,
                                    text="WIP: Reserved for second tool")

    #Positioning second tab widgets
    self.tab_2_frame.grid(column=0, row=0)
    self.tab_2_label.grid(column=0, row=0)

    self.notebook.add(self.tab_2_frame, text="WIP Tool")
    '''

    self.main_window.mainloop() #Starts the GUI event loop

  def select_file(self):
    '''
    Gets the filename and path of a user-selected file.
    Then it creates two pull-down menus for the user to chose graph labels.
    '''
    self.csv_filepath = tkFileDialog.askopenfilename(filetypes=[
                                                     ("CSV Files", "*.csv"),
                                                     ("All files","*.*")])

    if self.csv_filepath:
      print(self.csv_filepath)
      #Plotter backend retrieves list of possible graph labels
      self.column_headers = plotter_tool.get_csv_headers(self.csv_filepath)
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
    '''
    Gets the user's choice for the graph label and calls the plotter backend
    function. A plotted graph is output to a new window.

    Note that if the user doesn't close that graph and submits their options
    again, the plotter points will be plotted on top of the original graph.
    '''
    print('Submitted options, you should see a separate window with a')
    self.column_1_choice = self.column_options_1.get()
    self.column_2_choice = self.column_options_2.get()
    plotter_tool.submit_chosen_columns(self.csv_filepath, self.column_1_choice,
                                       self.column_2_choice)

  def setIcon(self, icon_name):
    '''
    Sets the favicon at top-leftmost of the Tkinter GUI

    Parameters
    ----------
    icon_name : str
      Filename of the icon to be used for the GUI

    Exceptions
    ----------
      If the icon can't be set, a warning outputs to the terminal
    '''
    try:
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