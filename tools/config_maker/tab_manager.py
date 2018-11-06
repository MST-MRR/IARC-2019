from tkinter import Frame, Button
from tkinter.ttk import Notebook

#from tools.config_maker.scroll_frame import VerticalScrolledFrame

from tools.config_maker.graph_node import GraphNode


class TabManager:
    def __init__(self, window):
        self._tab_controller = Notebook(window)
        self._tabs = []

        for text in ['Live Graphing Settings', 'After-The-Fact Graphing Settings']:
            self._tabs.append(Frame(self._tab_controller, bg="#66AA33"))
            self._tab_controller.add(self._tabs[-1], text=text)

        self._tab_controller.pack(expand=1, fill='both')

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

        graph = GraphNode(self.tab, len(self._graphs[section]), values={'lowerTime_chk': 'xxx', 'Pitch': True})

        graph.add_item('delete', (9, 0), Button(self.tab, text="Delete", command=lambda: self.delete(
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
            {'title': graph.name, 'lower_time': graph.items['lowerTime_chk'].get(),
             'upper_time': graph.items['upperTime_chk'].get(),
             'metric': [{
                 'label': metric.label, 'func': metric.raw_func, 'x_stream': metric.x_stream,
                 'y_stream': metric.y_stream, 'z_stream': metric.z_stream
             } for metric in graph.check_box_values.values() if metric.output.get()]
             }for graph in cur_graph]

    def share_settings(self):
        # Get all values -> same as save
        # Format and send to other tab

        print(self.sharing_settings)
