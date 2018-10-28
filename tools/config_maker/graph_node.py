from tkinter import *

from tools.file_io.file_io import possible_metrics

from tools.real_time_graphing.metric import Metric


class GraphNode:
    init_settings_filename = ["tools/config_maker/usable_metrics.xml", "usable_metrics.xml"]

    rows_per_graph = 3  # Baseline how many rows per graph

    checkbox_width = 6  # How many checkboxes allowed per line

    def __init__(self, tab, graph_num):

        #
        # Settings
        self.tab = tab
        self.graph_num = graph_num

        self.row_offset = self.graph_num * GraphNode.rows_per_graph

        self.height = GraphNode.rows_per_graph

        self.name = "Graph{}".format(self.graph_num)

        # Pull settings from hardcoded file

        check_box_settings = self.read_available_metrics()

        #
        # Item config
        self.item_locations = {}

        self.items = dict()

        # Header
        self.add_item('title', (0, 0, 2), Label(self.tab, text=self.name, font=("Arial Bold", 15), borderwidth=1))

        self.add_item('update_title', (2, 0, 2), Button(self.tab, text="Change Name", command=self.update_title, bd=2))

        # Check Boxes
        self.items['check_boxes'] = []
        self.check_box_values = [
            Metric(BooleanVar(), label=key, func=value[1], x_stream=value[0][0], y_stream=value[0][1], z_stream=value[0][2])
            for key, value in check_box_settings.items()]

        self.add_item('check_boxes', (1), [Checkbutton(self.tab, text=metric.label, var=metric.output) for metric in self.check_box_values])

        # Time interval settings
        self.add_item('lowerTime_lbl', (0, 2, 2), Label(self.tab, text="Time interval(seconds) Lower:", borderwidth=1))

        self.add_item('lowerTime_chk', (2, 2), Entry(self.tab, width=5))

        self.add_item('upperTime_lbl', (3, 2), Label(self.tab, text="Upper:", borderwidth=1))

        self.add_item('upperTime_chk', (4, 2), Entry(self.tab, width=5))

    def read_available_metrics(self):
        for filename in GraphNode.init_settings_filename:
            try:
                return possible_metrics(filename)
            except FileNotFoundError:
                pass

    def set_values(self):
        pass

    def add_check_box(self):
        # # TODO - Way to input custom functions - Add dynamic metrics

        # # TODO - Add metric button

        # self.check_box_values.update(
        # {Metric(None, label=key, func=value[1], x_stream=value[0][0], y_stream=value[0][1], z_stream=value[0][2]): BooleanVar()})

        # Need to add the tk checkbutton too!
        pass

    def delete(self):
        for key, value in self.items.items():
            if type(value) is list:
                for item in value:
                    item.destroy()
            else:
                value.destroy()

        return self

    def add_item(self, name, loc, obj):
        if type(obj) is list:
            for item in obj:
                item.configure(background="#66AA33")
        elif not type(obj) is Entry:
            obj.configure(background="#66AA33")

        self.items[name] = obj
        self.item_locations[name] = loc

    def set_grid(self, row_offset=None):
        if row_offset: self.row_offset = row_offset

        rolling_offset = self.row_offset  # If checkboxes take extra lines, the lines underneath will drop one

        # # TODO - Needs to be sorted by column, row too?

        for key, value in self.items.items():
            if key in self.item_locations:
                grid_values = self.item_locations[key]

                if type(value) is list:
                    for i in range(len(value)):
                        value[i].grid(sticky="W", column=i % GraphNode.checkbox_width,
                                      row=rolling_offset + grid_values + int(i / GraphNode.checkbox_width))

                    rolling_offset += int(len(value) / GraphNode.checkbox_width)
                else:
                    value.grid(column=grid_values[0], row=rolling_offset + grid_values[1],
                               columnspan=grid_values[2] if len(grid_values) > 2 else 1)

        self.height = rolling_offset + GraphNode.rows_per_graph

    def update_title(self):
        """
        Allows you to update the name of the graph
        """
        if isinstance(self.items['title'], Entry):
            self.name = self.items['title'].get()

            self.items['title'].destroy()

            self.items['title'] = Label(self.tab, text=self.name, font=("Arial Bold", 15), bg="#66AA33", borderwidth=1)

            self.items['update_title']['text'] = "Change Name"

        else:
            self.items['title'].destroy()

            self.items['title'] = Entry(self.tab, width=20)

            self.items['update_title']['text'] = "Submit"

        self.set_grid()