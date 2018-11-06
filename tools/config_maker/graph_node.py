from tkinter import *

from tools.file_io.file_io import possible_metrics

from tools.real_time_graphing.metric import Metric


# TODO - Way to input custom functions - Add dynamic metrics

# TODO - Add metric button

# TODO - Way to reference the lowerTime_chk and stuff like dat across modules

# TODO - Time settings getting appended rather than reset with share settings

# TODO - Finish reset function

# TODO - Catch error if get_data(tab_manager) is called while title is a textbox rather than a label

class GraphNode:
    init_settings_filename = ["tools/config_maker/usable_metrics.xml", "usable_metrics.xml"]

    rows_per_graph = 3  # Baseline how many rows per graph

    checkbox_width = 6  # How many checkboxes allowed per line

    class ItemList:
        def __init__(self):
            self.item_locations = {}
            self._items = {}

        @property
        def items(self):
            return self._items

        def __getitem__(self, item):
            return self._items[item]

        def __setitem__(self, key, value):
            self._items[key] = value

        def add_item(self, name, loc, obj):
            if type(obj) is dict:
                for item in obj.values():
                    item.configure(background="#66AA33")
            elif not type(obj) is Entry:
                obj.configure(background="#66AA33")

            self._items[name] = obj
            self.item_locations[name] = loc

    def __init__(self, tab, graph_num, values=None):
        #
        # Settings
        self.tab = tab
        self.graph_num = graph_num

        self.row_offset = self.graph_num * GraphNode.rows_per_graph

        self.height = GraphNode.rows_per_graph

        name = "Graph{}".format(self.graph_num)

        # Pull settings from hardcoded file
        check_box_settings = self.read_available_metrics()

        #
        # Item config
        self.items = GraphNode.ItemList()

        # Header
        self.items.add_item('title', (0, 0, 2), Label(self.tab, text=name, font=("Arial Bold", 15), borderwidth=1))

        self.items.add_item('update_title', (2, 0, 2), Button(self.tab, text="Change Name", command=self.update_title, bd=2))

        # Check Boxes
        self.items['check_boxes'] = {}
        self.check_box_values = {
            key: Metric(BooleanVar(), label=key, func=value[1], x_stream=value[0][0], y_stream=value[0][1], z_stream=value[0][2])
            for key, value in check_box_settings.items()}

        self.items.add_item('check_boxes', (1), {metric.label: Checkbutton(self.tab, text=metric.label, var=metric.output) for metric in self.check_box_values.values()})

        # Time interval settings
        self.items.add_item('lowerTime_lbl', (0, 2, 2), Label(self.tab, text="Time interval(seconds) Lower:", borderwidth=1))

        self.items.add_item('lowerTime_chk', (2, 2), Entry(self.tab, width=5))

        self.items.add_item('upperTime_lbl', (3, 2), Label(self.tab, text="Upper:", borderwidth=1))

        self.items.add_item('upperTime_chk', (4, 2), Entry(self.tab, width=5))

        if values: self.set_values(values)

    def read_available_metrics(self):
        for filename in GraphNode.init_settings_filename:
            try:
                return possible_metrics(filename)
            except FileNotFoundError:
                pass

    def reset(self, to_reset=None):
        # TODO - Add default item settings
        if type(to_reset) is not list: to_reset = [to_reset]
        if not to_reset: to_reset = [key for key in self.items.keys()]

        for item in to_reset:
            if item == 'check_boxes':
                for value in self.check_box_values.values():
                    value.output.set(False)

    def set_values(self, values):
        self.reset('check_boxes')

        for name, value in values.items():
            if name in self.items.items:
                if isinstance(self.items[name], Label):
                    self.items[name]['text'] = value
                elif isinstance(self.items[name], Entry):
                    self.items[name].insert(20, value)
                else:
                    self.items[name].set(value)
            elif name in self.check_box_values.keys():
                self.check_box_values[name].output.set(value)

    def add_check_box(self):
        # self.check_box_values.update(
        # {Metric(None, label=key, func=value[1], x_stream=value[0][0], y_stream=value[0][1], z_stream=value[0][2]): BooleanVar()})

        # Need to add the tk checkbutton too!
        pass

    def delete(self):
        for value in self.items.values():
            if type(value) is dict:
                for item in value.values():
                    item.destroy()
            else:
                value.destroy()

        return self



    def set_grid(self, row_offset=None):
        if row_offset: self.row_offset = row_offset

        rolling_offset = self.row_offset  # If checkboxes take extra lines, the lines underneath will drop one

        for key, value in self.items.items.items():
            if key in self.items.item_locations.keys():
                grid_values = self.items.item_locations[key]

                if type(value) is dict:
                    for i, key in enumerate(value.keys()):
                        value[key].grid(sticky="W", column=i % GraphNode.checkbox_width,
                                        row=rolling_offset + grid_values + int(i / GraphNode.checkbox_width))

                    rolling_offset += int(len(value) / GraphNode.checkbox_width)
                else:
                    value.grid(column=grid_values[0],
                               row=grid_values[1] + rolling_offset if grid_values[1] > 1 else self.row_offset,
                               columnspan=grid_values[2] if len(grid_values) > 2 else 1)

        self.height = rolling_offset + GraphNode.rows_per_graph

    def update_title(self):
        """
        Allows you to update the name of the graph
        """
        if isinstance(self.items['title'], Entry):
            name = self.items['title'].get()

            self.items['title'].destroy()

            self.items['title'] = Label(self.tab, text=name, font=("Arial Bold", 15), bg="#66AA33", borderwidth=1)

            self.items['update_title']['text'] = "Change Name"

        else:
            self.items['title'].destroy()

            self.items['title'] = Entry(self.tab, width=20)

            self.items['update_title']['text'] = "Submit"

        self.set_grid()
