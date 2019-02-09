'''
Python ver 3.7.1
This is a GUI for any tools that require one, such as the plotter that graphs
csv files and a config maker to customize graphs.

NOTE: There is a test file under tools/test/test_csv to test out the plotter.
TODO: Create a unit test for the GUI
'''
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog
import logging, os
#Importing the plotter backend.
import plotter.plotter_backend as plotter_tool

class MultiToolGUI:
  '''
  A class used to represent the GUI for the plotter (and future tools).

  Methods
  -------
  select_file()
    Gets the user chosen filename and filepath and creates widgets for the
    user to choose their graph labels in a drop-down menu
  submit_graph_options()
    Retrieves user-selected graph labels and plots a graph
  set_icon()
    Sets the GUI favicon
  '''
  #Class constants
  ICON_ERROR_MESSAGE = "Unable to set the icon for the program."
  ICON_NAME = 'ninja_icon.gif'
  #Builds a filepath based to the icon
  ICON_PATH = os.path.join(os.path.dirname(__file__), ICON_NAME)
  #Only two variables can be graphed by the plotter as of right now
  NUM_COLUMN_OPTIONS = 2
  

  def __init__(self):
    self.main_window = tk.Tk() #Creates the application window
    self.main_window.title("MST Multirotor Multitool")
    #TODO Convert ninga_icon.gif to an .ico file
    self.set_icon(self.ICON_PATH)

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

    #TODO Make the drone swarm controller simulator for the second tab

    self.main_window.mainloop() #Starts the GUI event loop

  def select_file(self):
    '''
    Gets the filename and path of a user-selected file.
    Then it creates two pull-down menus for the user to chose graph labels.
    '''
    self.csv_filepath = tkinter.filedialog.askopenfilename(filetypes=[
                                                     ("CSV Files", "*.csv"),
                                                     ("All files","*.*")])

    if self.csv_filepath:
      logging.debug("Icon filepath at: " + self.csv_filepath)
      #Plotter backend retrieves list of possible graph labels
      self.column_headers = plotter_tool.get_csv_headers(self.csv_filepath)

      #Creates widgets for number of column options
      for column_index in range(self.NUM_COLUMN_OPTIONS):
        attr_name = 'column_options{}'.format(column_index)
        combobox = ttk.Combobox(self.plotter_frame, values=self.column_headers)

        #Widget positioning
        setattr(self, attr_name, combobox)
        getattr(self, attr_name).grid(column=column_index, row=2)

      self.plotter_submit_button = ttk.Button(self.plotter_frame,
                                              text="Submit",
                                              command=self.submit_graph_options)
      self.plotter_submit_button.grid(columnspan=2, row=3)

  def submit_graph_options(self):
    '''
    Gets the user's choice for the graph label and calls the plotter backend
    function. A plotted graph is output to a new window.

    Note that if the user doesn't close that graph and submits their options
    again, the plotter points will be plotted on top of the original graph.
    '''
    logging.info('Submitted options, you should see a separate window with a')

    plotter_tool.submit_chosen_columns(self.csv_filepath, self.column_options0.get(),
                                       self.column_options1.get())

  def set_icon(self, icon_path):
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
      #Cannot be set before init since it calls a tk method
      self.icon_img = tk.PhotoImage(file=icon_path)
      self.main_window.iconbitmap(self.icon_img)
      logging.info("Icon set successful, check the top-left part of the GUI!")
    except tk.TclError:
      #tk.TclError is the error raised when the icon file can't be found
      #or if the wrong filetype is used (anything not .ico)
      logging.error(self.ICON_ERROR_MESSAGE)

if __name__ == '__main__':
  #Initializes the class and creates the application
  MultiToolGUI()