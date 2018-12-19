from tkinter import Frame, Button
from tkinter.ttk import Notebook

try:
    from tools.config_maker.graph_node import GraphNode
except ImportError:
    from graph_node import GraphNode

class TabManager:
    """
    Interface for interacting with tabs.

    Parameters
    ----------
    window: tkinter window
        Window tabs should be placed in.
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
        """
        Current tab frame getter

        Returns
        -------
        Frame of current tab.
        """

        return self._tabs[self.tab_id]

    @property
    def tab_id(self):
        """
        Current tab index getter

        Returns
        -------
        Index of current tab.
        """

        return self._tab_controller.index("current")

    @property
    def curr_tab_graphs(self):
        """
        Current tab graphs getter

        Returns
        -------
        List of graphs from current tab.
        """

        return self._graphs[self.tab_id]

    def __getitem__(self, item):
        """
        Current tab graphs getter. Operator[].

        Returns
        -------
        List of graphs from current tab.
        """

        return self._graphs[item]

    # GraphNode functions
    def add_graph(self, section=None):
        """
        Add graph to tab

        Parameters
        ----------
        section: number, default=None
            Tab index to add graph into, if none section=current tab id.
        """

        if not section: section = self.tab_id

        graph = GraphNode(self.tab, len(self._graphs[section]))

        graph.add_item('delete', (9, 0), Button(self.tab, text="Delete", command=lambda: self.delete_graph(
            graph=graph), bd=2))

        self.curr_tab_graphs.append(graph)

        self.update_graph_positions()

    def delete_graph(self, section=None, graph=None):
        """
        Delete graph from tab.

        Parameters
        ----------
        section: number, default=None
            Tab index to delete graph from, if none section=current tab id.

        graph: number, default=None
            Graph index to delete, if none graph=last graph index.
        """

        if len(self._graphs[self.tab_id]) is 0: return

        if not section: section = self.tab_id
        if not graph: graph = self._graphs[section][-1]

        self.curr_tab_graphs.remove(graph.delete())

        self.update_graph_positions()

    def update_graph_positions(self):
        """
        Updates all graphs position based on above graphs height
        """

        for frame in self._graphs:
            curr_offset = 0
            for graph in frame:
                graph.set_grid(curr_offset)

                curr_offset += graph.height

    def get_graph_data(self, tab_id=None):
        """
        Get all data from selected tab

        Parameters
        ----------
        tab_id: number, default=None
            Tab index to get data from, if none tab_id=current tab id.

        Returns
        -------
        Data of tab in form of dictionary
        """
        cur_graph = self._graphs[tab_id] if tab_id else self.curr_tab_graphs

        return [
            {'title': graph.items['title']['text'], 'lower_time': graph.items['lowerTime_chk'].get(),
             'upper_time': graph.items['upperTime_chk'].get(),
             'metric': [{
                 'label': metric.label, 'func': metric.raw_func, 'x_stream': metric.x_stream,
                 'y_stream': metric.y_stream, 'z_stream': metric.z_stream
             } for metric in graph.check_box_values.values() if metric.output.get()]
             }for graph in cur_graph]
