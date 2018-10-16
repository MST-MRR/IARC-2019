from tkinter import *
from tkinter import ttk
import csv


class GraphSettings:
    rows_per_graph = 3

    def __init__(self, tab, graph_num):
        # TODO - Work on design of gui

        # TODO - Delete graph button

        # TODO - Way to input custom functions - Add dynamic metrics

        # TODO - Pull possible(hardcoded) metrics from file and put into checkboxes

        # TODO - Make checkboxes get pushed down a line if necessary

        #
        # Settings
        self.tab = tab
        self.graph_num = graph_num

        self.row_offset = self.graph_num * GraphSettings.rows_per_graph

        self.name = "Graph{}".format(self.graph_num)

        #
        # Items
        self.item_locations = {'grph_lbl': (0, 0, 2), 'update_Name_btn': (2, 0, 2), 'lowerTime_lbl': (0, 2, 2),
                                'lowerTime_chk': (2, 2), 'upperTime_lbl': (3, 2), 'upperTime_chk': (4, 2)}

        self.items = dict()

        self.items['grph_lbl'] = Label(self.tab, text=self.name, font=("Arial Bold", 15))  # graph label

        # Update header
        self.items['update_Name_btn'] = Button(self.tab, text="Change Name", command=self.ChangeName)

        #
        # Setup check mark buttons
        self.items['check_boxes'] = []
        self.check_box_values = {}

        self.generate_check_boxes(self.tab, self.row_offset + 1)

        #
        # Time interval settings
        self.items['lowerTime_lbl'] = Label(self.tab, text="Time interval(seconds) Lower:")

        self.items['lowerTime_chk'] = Entry(self.tab, width=5)

        self.items['upperTime_lbl'] = Label(self.tab, text="Upper:")

        self.items['upperTime_chk'] = Entry(self.tab, width=5)

        self.set_grid()

    def set_grid(self):
        for key, value in self.items.items():
            if key in self.item_locations:
                grid_values = self.item_locations[key]

                value.grid(column=grid_values[0], row=self.row_offset + grid_values[1],
                           columnspan=grid_values[2] if len(grid_values) > 2 else 1)

    def generate_check_boxes(self, tab, row):
        check_box_settings = ["Air Speed", "Altitude", "Pitch", "Roll", "Yaw", "xVelocity", "yVelocity", "zVelocity",
                              "Voltage"]

        i = 0

        # Chose this format because I don't think we will ever care about individual checkboxes values, only quick
        # iteration through the list to save
        for key in check_box_settings:
            self.check_box_values.update({key: BooleanVar()})
            self.items['check_boxes'].append(Checkbutton(tab, text=key, var=self.check_box_values[key]))

            self.items['check_boxes'][-1].grid(column=i, row=row)
            i += 1

    def ChangeName(self):
        if isinstance(self.grph_lbl, Entry):
            self.name = self.grph_lbl.get()

            self.grph_lbl.destroy()

            self.grph_lbl = Label(self.tab, text=self.name, font=("Arial Bold", 15))  # graph label
            self.grph_lbl.grid(column=0, row=self.row_offset, columnspan=2)

            self.update_Name_btn['text'] = "Change Name"

        else:
            self.grph_lbl.destroy()

            self.grph_lbl = Entry(self.tab, width=20)
            self.grph_lbl.grid(column=0, row=self.row_offset, columnspan=2)

            self.update_Name_btn['text'] = "Submit"


class GUI:
    # Config output files
    settings_file = "GUI_Settings.csv"

    def __init__(self):
        # TODO - pull old settings into window if possible

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

        # TODO - Make know what tab is currently being looked at and save to according file & apply global functions
        #           only to that tab

        #
        # Create initial graphs
        self.graphs = [GraphSettings(self.tab1, i) for i in range(2)]

        #
        # Global Buttons
        self.update_grph_btn = Button(self.tab1, text="Click to Update Section", command=self.save)
        self.update_grph_btn.grid(column=4, row=0, columnspan=2)

        # TODO - add more global buttons
        # Reset button
        # Push data to other tab button
        # Add graph button

        #
        # Display window
        tab_control.pack(expand=1, fill='both')#should be near the end?
        window.mainloop()#this needs to be at the end

    def save(self):
        # using the csv for the GUI
        with open(GUI.settings_file, 'w') as g:
            for graph in self.graphs:
                StatusDict = {"Status_GraphName": graph.name, "Status_lowerTime": graph.lowerTime_chk.get(),
                              "Status_upperTime": graph.upperTime_chk.get()}

                StatusDict.update({"Status_{}".format(key): 1 if value.get() else 0 for key, value in graph.check_box_values.items()})

                for key, value in StatusDict.items():
                    g.write("{} = {}\n".format(key, str(value)))

                g.write("\n")


if __name__ == "__main__":
    myClass = GUI()
