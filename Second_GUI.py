from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import csv


class GraphSettings:
    rows_per_graph = 3  # Baseline how many rows per graph

    checkbox_width = 3  # How many checkboxes allowed per line

    def __init__(self, tab, graph_num):
        # TODO - Work on design of gui

        # TODO - Delete graph button

        # TODO - Way to input custom functions - Add dynamic metrics

        # TODO - Pull possible(hardcoded) metrics from file and put into checkboxes

        # TODO - Add metric button

        #
        # Settings
        self.tab = tab
        self.graph_num = graph_num

        self.row_offset = self.graph_num * GraphSettings.rows_per_graph

        self.height = GraphSettings.rows_per_graph

        self.name = "Graph{}".format(self.graph_num)

        #
        # Item config
        self.item_locations = {'title': (0, 0, 2), 'update_title': (2, 0, 2), 'lowerTime_lbl': (0, 2, 2),
                               'lowerTime_chk': (2, 2), 'upperTime_lbl': (3, 2), 'upperTime_chk': (4, 2),
                               'check_boxes': (1)}

        self.items = dict()

        def add_item(name, loc):
            pass

        # Header
        self.items['title'] = Label(self.tab, text=self.name, font=("Arial Bold", 15))

        self.items['update_title'] = Button(self.tab, text="Change Name", command=self.update_title)

        # Setup check mark buttons
        self.items['check_boxes'] = []
        self.check_box_values = {}

        self.generate_check_boxes()

        # Time interval settings
        self.items['lowerTime_lbl'] = Label(self.tab, text="Time interval(seconds) Lower:")

        self.items['lowerTime_chk'] = Entry(self.tab, width=5)

        self.items['upperTime_lbl'] = Label(self.tab, text="Upper:")

        self.items['upperTime_chk'] = Entry(self.tab, width=5)

    def set_grid(self, row_offset=None):
        if row_offset: self.row_offset = row_offset

        rolling_offset = self.row_offset  # If checkboxes take extra lines, the lines underneath will drop one

        for key, value in self.items.items():
            if key in self.item_locations:
                grid_values = self.item_locations[key]

                if type(value) is list:
                    for i in range(len(value)):
                        value[i].grid(column=i % GraphSettings.checkbox_width,
                                      row=rolling_offset + grid_values + int(i / GraphSettings.checkbox_width))

                    rolling_offset += int(len(value) / GraphSettings.checkbox_width) - 1
                else:
                    value.grid(column=grid_values[0], row=rolling_offset + grid_values[1],
                               columnspan=grid_values[2] if len(grid_values) > 2 else 1)

        self.height = rolling_offset + GraphSettings.rows_per_graph

    def pull_check_box_settings(self):
        return ["Air Speed", "Altitude", "Pitch", "Roll", "Yaw", "xVelocity", "yVelocity", "zVelocity", "Voltage"]

    def generate_check_boxes(self):
        check_box_settings = self.pull_check_box_settings()

        for key in check_box_settings:
            self.check_box_values.update({key: BooleanVar()})
            self.items['check_boxes'].append(Checkbutton(self.tab, text=key, var=self.check_box_values[key]))

    def update_title(self):
        if isinstance(self.items['title'], Entry):
            self.name = self.items['title'].get()

            self.items['title'].destroy()

            self.items['title'] = Label(self.tab, text=self.name, font=("Arial Bold", 15))  # graph label

            self.items['update_title']['text'] = "Change Name"

        else:
            self.items['title'].destroy()

            self.items['title'] = Entry(self.tab, width=20)

            self.items['update_title']['text'] = "Submit"

        self.set_grid()


class GUI:

    # Config output files
    settings_file = "GUI_Settings.csv"

    def __init__(self):
        # TODO - pull old settings into window

        #
        # Window setup
        window = Tk()
        window.title("Multirotor Robot Data Graphing Tool")
        window.geometry('750x500')

        icon = PhotoImage(file='ninja_icon.gif')
        window.tk.call('wm', 'iconphoto', window._w, icon)

        #
        # Menu Making
        self.bar = Menu(window)
        self.bar.add_command(label='Pick a file',command=GUI.pick_graphing_file)
        self.bar.add_command(label="Add new graph")
        self.bar.add_command(label="Delete Last Graph")
        self.bar.add_command(label="Reset Selections")
        #self.bar.add_command(label="Copy Settings to both tabs?") #not sure how to implement this


        #
        # Separate tabs
        self.tab_control = ttk.Notebook(window)

        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text='Live Graphing Settings')
        self.tab_control.add(self.tab2, text='After-The-Fact Graphing Settings')

        self.tab_control.pack(expand=1, fill='both')

        # TODO - Make know what tab is currently being looked at and save to according file & apply global functions
        #           only to that tab

        #
        # Create initial graphs
        self.graphs = [GraphSettings(self.tab1, i) for i in range(2)]

        self.update_offsets()

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
        window.config(menu=self.bar)
        window.mainloop()

    def pick_graphing_file():
        self.data_file = filedialog.askopenfilename(
        title="Select file to Graph", filetypes=(("csv files", "*.csv"), ("all files", "*.*"))
        )

    def update_offsets(self):
        curr_offset = 0

        for graph in self.graphs:
            graph.set_grid(curr_offset)

            curr_offset += graph.height

    def save(self):

        # TODO - Format saving into xml

        # using the csv for the GUI
        with open(GUI.settings_file, 'w') as g:
            for graph in self.graphs:
                output = {"Status_GraphName": graph.name, "Status_lowerTime": graph.items['lowerTime_chk'].get(),
                          "Status_upperTime": graph.items['upperTime_chk'].get()}

                output.update({"Status_{}".format(key): 1 if value.get() else 0 for key, value in graph.check_box_values.items()})

                for key, value in output.items():
                    g.write("{} = {}\n".format(key, str(value)))

                g.write("\n")


if __name__ == "__main__":
    myClass = GUI()
