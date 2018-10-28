from tkinter import *
from tkinter import ttk, filedialog

from tools.config_maker.graph_node import GraphNode

from tools.file_io.file_io import write_config


# https://gist.github.com/EugeneBakin/76c8f9bcec5b390e45df
# TODO -------- make work? Maybe make this create a frame and canvas and buttons get put on frame grid

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)

        # TODO - Make scrollbar align right without using pack

        #vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)

        vscrollbar.grid(column=10, rowspan=10)

        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)

        # TODO - Separate canvas and scrollbar?, sticky?
        #canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        #canvas.grid(column=0)

        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


class GUI:
    settings_file = "GUI_Settings.xml"  # Config output

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

    def __init__(self):
        # # TODO - pull old settings into window

        self.data_file = None

        #
        # Window setup
        window = Tk()
        window.title("Multirotor Robot Data Graphing Tool")
        window.geometry('750x500')

        try:
            icon = PhotoImage(file='ninja_icon.gif')
            window.tk.call('wm', 'iconphoto', window._w, icon)

        except TclError:
            print("Failed to open icon")

        #
        # Separate tabs
        self.tab_control = ttk.Notebook(window)  # TODO - Could maybe just put in GraphStorage
        self.tabs = []

        for text in ['Live Graphing Settings', 'After-The-Fact Graphing Settings']:
            self.tabs.append(VerticalScrolledFrame(self.tab_control, bg="#66AA33"))
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

        self.menu_bar = Menu(window, fg="#66AA33")

        self.menu_bar.add_command(label='Pick a file', command=self.pick_graphing_file)

        self.menu_bar.add_command(label="Add new graph", command=self.graphs.add)
        self.menu_bar.add_command(label="Delete Last Graph", command=self.graphs.delete)

        self.menu_bar.add_command(label="Pull old config")

        self.menu_bar.add_command(label="Reset Selections")

        self.menu_bar.add_command(label="Save", command=self.save)

        self.menu_bar.add_checkbutton(label="Share tab settings", var=self.sharing_settings,
                                      command=self.toggle_sharing)  # not sure how to implement this

        # # TODO - Make copy settings toggleable by highlighting background differently

        #
        # Display window
        window.config(menu=self.menu_bar)
        window.mainloop()

    def toggle_sharing(self):
        # # TODO - Make share settings to both config(tabs)

        print(self.sharing_settings)

    def pick_graphing_file(self):
        # # TODO - How to save this data?
        # # TODO - Make data get read and used

        self.data_file = filedialog.askopenfilename(
            title="Select file to Graph", filetypes=(("csv files", "*.csv"), ("all files", "*.*"))
        )

    def save(self, section=None):
        # # TODO - Chose where to save based on tab !

        graphs = self.graphs[section] if section else self.graphs.curr

        total_output = [
            {'title': graph.name, 'lower_time': graph.items['lowerTime_chk'].get(),
             'upper_time': graph.items['upperTime_chk'].get(),
             'metric': [{'label': metric.label, 'func': metric.raw_func, 'x_stream': metric.x_stream,
                         'y_stream': metric.y_stream, 'z_stream': metric.z_stream}
                        for metric in graph.check_box_values if metric.output.get()]}
            for graph in graphs]

        write_config(GUI.settings_file, total_output)


if __name__ == "__main__":
    myClass = GUI()
