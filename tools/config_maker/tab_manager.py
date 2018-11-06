from tkinter import Frame, Button, filedialog
from tkinter.ttk import Notebook

#from tools.config_maker.scroll_frame import VerticalScrolledFrame

from tools.config_maker.graph_node import GraphNode


# TODO -> should get data be put in graph node


class TabManager:
    """
    TODO - Hold no customization except what will never change
    TODO - An interface to interact with tabs and the graph nodes contained within
    TODO - Should only manage graph nodes
    """

    def __init__(self, window):
        self._tab_controller = Notebook(window)
        self._tabs = []

        for text in ['Live Graphing Settings', 'After-The-Fact Graphing Settings']:
            self._tabs.append(Frame(self._tab_controller, bg="#66AA33"))
            self._tab_controller.add(self._tabs[-1], text=text)

        self._tab_controller.pack(expand=1, fill='both')

        self._graphs = [[], []]

    # Tab functions
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

    # GraphNode functions
    def append(self, value):
        self._graphs.curr.append(value)
        self.update()

    def add(self, section=None):
        if not section: section = self.tab_id

        graph = GraphNode(self.tab, len(self._graphs[section]), values={'lowerTime_chk': 'xxx', 'Pitch': True})

        graph.items.add_item('delete', (9, 0), Button(self.tab, text="Delete", command=lambda: self.delete(
            graph=graph), bd=2))

        self.curr.append(graph)

        self.update()

    def delete(self, section=None, graph=None):
        if len(self._graphs[self.tab_id]) is 0: return

        if not section: section = self.tab_id
        if not graph: graph = self._graphs[section][-1]

        self.curr.remove(graph.delete())

        self.update()

    def update(self):
        for frame in self._graphs:
            curr_offset = 0
            for graph in frame:
                graph.set_grid(curr_offset)

                curr_offset += graph.height

    def get_data(self, tab_id=None):
        cur_graph = self._graphs[tab_id] if tab_id else self.curr

        return [
            {'title': graph.items['title']['text'], 'lower_time': graph.items['lowerTime_chk'].get(),
             'upper_time': graph.items['upperTime_chk'].get(),
             'metric': [{
                 'label': metric.label, 'func': metric.raw_func, 'x_stream': metric.x_stream,
                 'y_stream': metric.y_stream, 'z_stream': metric.z_stream
             } for metric in graph.check_box_values.values() if metric.output.get()]
             }for graph in cur_graph]

    #
    # TODO - how to classify
    def share_settings(self, base_tab_id=None, dest_tab_id=None):
        # Get all values -> same as save
        # Format and send to other tab
        data = self.get_data(base_tab_id)

        if dest_tab_id:
            relevant_tabs = dest_tab_id if type(dest_tab_id) is list else [dest_tab_id]
        else:
            relevant_tabs = [i for i in range(len(self._tabs)) if i is not base_tab_id]

        for tab in (self[i] for i in relevant_tabs):
            for i, row in enumerate(data):
                if len(tab) > i:
                    val = {'title': row['title'], 'lowerTime_chk': row['lower_time'], 'upperTime_chk': row['upper_time']}
                    val.update({metric['label']: True for metric in row['metric']})

                    tab[i].set_values(val)

    def pick_graphing_file(self):
        # # TODO - How to save this data?
        # # TODO - Make data get read and used

        self.data_file = filedialog.askopenfilename(
            title="Select file to Graph", filetypes=(("csv files", "*.csv"), ("all files", "*.*"))
        )
