from tkinter import *
from tkinter import ttk, filedialog

from tools.file_io.file_io import possible_metrics, write_config

from tools.real_time_graphing.metric import Metric


class GraphSettings:
    init_settings_filename = "usable_metrics.xml"

    rows_per_graph = 3  # Baseline how many rows per graph

    checkbox_width = 6  # How many checkboxes allowed per line

    def __init__(self, tab, graph_num):

        # TODO - Way to input custom functions - Add dynamic metrics

        # TODO - Add metric button

        #
        # Settings
        self.tab = tab
        self.graph_num = graph_num

        self.row_offset = self.graph_num * GraphSettings.rows_per_graph

        self.height = GraphSettings.rows_per_graph

        self.name = "Graph{}".format(self.graph_num)

        # Pull settings from hardcoded file

        check_box_settings = self.read_init_settings()

        #
        # Item config
        self.item_locations = {}

        self.items = dict()

        # Header
        self.add_item('title', (0, 0, 2), Label(self.tab, text=self.name, font=("Arial Bold", 15)))

        self.add_item('update_title', (2, 0, 2), Button(self.tab, text="Change Name", command=self.update_title))

        # Check Boxes
        self.items['check_boxes'] = []
        self.check_box_values = {}  # TODO - Change to list of Metrics

        self.check_box_values.update({
            Metric(None, label=key, func=value[1], x_stream=value[0][0], y_stream=value[0][1], z_stream=value[0][2]):
                BooleanVar() for key, value in check_box_settings.items()})

        self.add_item('check_boxes', (1), [Checkbutton(self.tab, text=key.label, var=self.check_box_values[key]) for key in self.check_box_values])

        # Time interval settings
        self.add_item('lowerTime_lbl', (0, 2, 2), Label(self.tab, text="Time interval(seconds) Lower:"))

        self.add_item('lowerTime_chk', (2, 2), Entry(self.tab, width=5))

        self.add_item('upperTime_lbl', (3, 2), Label(self.tab, text="Upper:"))

        self.add_item('upperTime_chk', (4, 2), Entry(self.tab, width=5))

    def read_init_settings(self):
        return possible_metrics(self.init_settings_filename)

    def set_values(self):
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
        self.items[name] = obj
        self.item_locations[name] = loc

    def set_grid(self, row_offset=None):
        if row_offset: self.row_offset = row_offset

        rolling_offset = self.row_offset  # If checkboxes take extra lines, the lines underneath will drop one

        for key, value in self.items.items():
            if key in self.item_locations:
                grid_values = self.item_locations[key]

                if type(value) is list:
                    for i in range(len(value)):
                        value[i].grid(sticky="W", column=i % GraphSettings.checkbox_width,
                                      row=rolling_offset + grid_values + int(i / GraphSettings.checkbox_width))

                    rolling_offset += int(len(value) / GraphSettings.checkbox_width)
                else:
                    value.grid(column=grid_values[0], row=rolling_offset + grid_values[1],
                               columnspan=grid_values[2] if len(grid_values) > 2 else 1)

        self.height = rolling_offset + GraphSettings.rows_per_graph

    def update_title(self):
        if isinstance(self.items['title'], Entry):
            self.name = self.items['title'].get()

            self.items['title'].destroy()

            self.items['title'] = Label(self.tab, text=self.name, font=("Arial Bold", 15))

            self.items['update_title']['text'] = "Change Name"

        else:
            self.items['title'].destroy()

            self.items['title'] = Entry(self.tab, width=20)

            self.items['update_title']['text'] = "Submit"

        self.set_grid()


class GUI:
    settings_file = "GUI_Settings.csv"  # Config output

    class GraphStorage:
        def __init__(self, tab_controller, tabs):
            self._tab_controller = tab_controller

            self._tabs = tabs

            self._graphs = [[], []]

        @property
        def tab(self):
            return self._tabs[self.tab_id]

        @property
        def tab_id(self):
            return self._tab_controller.index("current")

        @property
        def curr(self):
            return self._graphs[self.tab_id]

        def __getitem__(self, item):
            return self._graphs[item]

        def append(self, value):
            self._graphs.curr.append(value)
            self.update()

        def add(self, section=None):
            if not section: section = self.tab_id

            graph = GraphSettings(self.tab, len(self._graphs[section]))

            graph.add_item('delete', (9, -1), Button(self.tab, text="Delete", command=lambda: self.delete(
                graph=graph)))  # TODO - Fix -1 thing

            self.curr.append(graph)

            self.update()

        def delete(self, section=None, graph=None):
            if len(self._graphs[self.tab_id]) is 0: return

            if not section: section = self.tab_id
            if not graph: graph = self._graphs[section][-1]

            self.curr.remove(graph.delete())

            self.update()

        def update(self):
            curr_offset = 0

            for frame in self._graphs:
                for graph in frame:
                    graph.set_grid(curr_offset)

                    curr_offset += graph.height

    def __init__(self):
        # TODO - pull old settings into window

        self.data_file = None

        #
        # Window setup
        window = Tk()
        window.title("Multirotor Robot Data Graphing Tool")
        window.geometry('750x500')

        icon = PhotoImage(file='../../ninja_icon.gif')
        window.tk.call('wm', 'iconphoto', window._w, icon)

        #
        # Separate tabs
        self.tab_control = ttk.Notebook(window)
        self.tabs = []

        for text in ['Live Graphing Settings', 'After-The-Fact Graphing Settings']:
            self.tabs.append(ttk.Frame(self.tab_control))
            self.tab_control.add(self.tabs[-1], text=text)

        self.tab_control.pack(expand=1, fill='both')

        #
        # Create initial graphs
        self.graphs = GUI.GraphStorage(self.tab_control, self.tabs)
        for i in range(2): self.graphs.add()

        #
        # Menu Making
        self.sharing_settings = 0
        # self.sharing_color = "green"

        self.menu_bar = Menu(window)

        self.menu_bar.add_command(label='Pick a file', command=self.pick_graphing_file)

        self.menu_bar.add_command(label="Add new graph", command=self.graphs.add)
        self.menu_bar.add_command(label="Delete Last Graph", command=self.graphs.delete)

        self.menu_bar.add_command(label="Pull old config")

        self.menu_bar.add_command(label="Reset Selections")

        self.menu_bar.add_command(label="Save", command=self.save)

        self.menu_bar.add_checkbutton(label="Share tab settings", var=self.sharing_settings,
                                      command=self.toggle_sharing)  # not sure how to implement this
        # TODO - Make copy settings toggleable by highlighting background differently

        #
        # Display window
        window.config(menu=self.menu_bar)
        window.mainloop()

    @property
    def tab(self):
        return self.tabs[self.tab_id]

    @property
    def tab_id(self):
        return self.tab_control.index("current")

    def toggle_sharing(self):
        # TODO - Make share settings to both config(tabs)

        print(self.sharing_settings)

    def pick_graphing_file(self):
        self.data_file = filedialog.askopenfilename(
            title="Select file to Graph", filetypes=(("csv files", "*.csv"), ("all files", "*.*"))
        )

    def save(self, section=None):
        if not section: section = self.tab_id

        total_output = []
        """
        for graph in self.graphs[section]:
            output = {"Status_GraphName": graph.name, "Status_lowerTime": graph.items['lowerTime_chk'].get(),
                      "Status_upperTime": graph.items['upperTime_chk'].get()}

            output.update(
                {"Status_{}".format(key): 1 if value.get() else 0 for key, value in graph.check_box_values.items()})

            total_output.append(output)
        """
        # Looking for list of dicts of graphs w/ all tags containing list of dicts of metrics
        for graph in self.graphs[section]:
            output = {"title": graph.name, "lower_time": graph.items['lowerTime_chk'].get(),
                      "upper_time": graph.items['upperTime_chk'].get(), 'metric': []}

            for metric, value in graph.check_box_values.items():
                if value.get():
                    output['metric'].append({'label': metric.label, 'func': metric.raw_func,
                                        'x_stream': metric.x_stream, 'y_stream': metric.y_stream,
                                        'z_stream': metric.z_stream})

            total_output.append(output)

        # Realtime grapher should assume x and y label if not given and have more colors
        # Graph -> title, x_label, y_label
        # Needs label, func, streams

        write_config(GUI.settings_file, total_output)


if __name__ == "__main__":
    myClass = GUI()
