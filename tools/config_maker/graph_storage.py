from tkinter import *

from tools.config_maker.graph_node import GraphNode


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

        graph = GraphNode(self.tab, len(self._graphs[section]))

        graph.add_item('delete', (9, -1), Button(self.tab, text="Delete", command=lambda: self.delete(
            graph=graph), bd=2))  # TODO - Fix -1 thing

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