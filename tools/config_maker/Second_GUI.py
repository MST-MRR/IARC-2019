from tkinter import *
from tkinter import ttk, filedialog

#from tools.config_maker.scroll_frame import VerticalScrolledFrame
from tools.config_maker.graph_storage import GraphStorage

from tools.file_io.file_io import write_config


# TODO - pull old settings into window

# TODO - Way to save what file you want graphed

# TODO - Make share settings to both config(tabs)

# TODO - Fix file_io problems based on where program is called from

# TODO - add var for icon filename

# TODO - put tab creation in GraphStorage?

# # TODO - Make copy settings toggleable by highlighting button background differently

# # TODO - Chose where to save based on tab ! and set variable to set it


class GUI:
    settings_file = "GUI_Settings.xml"  # Config output file

    def __init__(self):
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
        self.tab_control = ttk.Notebook(window)
        self.tabs = []

        for text in ['Live Graphing Settings', 'After-The-Fact Graphing Settings']:
            self.tabs.append(Frame(self.tab_control, bg="#66AA33"))
            self.tab_control.add(self.tabs[-1], text=text)

        self.tab_control.pack(expand=1, fill='both')

        #
        # Create initial graphs
        self.graphs = GraphStorage(self.tab_control, self.tabs)
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
                                      command=self.toggle_sharing)

        #
        # Display window
        window.config(menu=self.menu_bar)
        window.mainloop()

    def toggle_sharing(self):
        print(self.sharing_settings)

    def pick_graphing_file(self):
        # # TODO - How to save this data?
        # # TODO - Make data get read and used

        self.data_file = filedialog.askopenfilename(
            title="Select file to Graph", filetypes=(("csv files", "*.csv"), ("all files", "*.*"))
        )

    def save(self, section=None):
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
