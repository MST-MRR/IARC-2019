from tkinter import *
from tkinter import filedialog

from tools.config_maker.tab_manager import TabManager

from tools.file_io.file_io import write_config


# TODO - Implement scrolled frame

# TODO - pull old settings into window

# TODO - Way to save what file you want graphed
# TODO - Chose where to save based on tab ! and set variable to set it

# TODO - Fix file_io problems based on where program is called from
# TODO - File_io detect where program is being called from and add necessary directories

# TODO - Tab configurations to set names, disable parts for each


class GUI:
    settings_file = "Flight_Num.xml"  # Config output file

    icon_file = '../../ninja_icon.gif'

    def __init__(self):
        self.data_file = None

        #
        # Window setup
        window = Tk()
        window.title("Multirotor Robot Data Graphing Tool")
        window.geometry('750x500')

        try:
            icon = PhotoImage(file=GUI.icon_file)
            window.tk.call('wm', 'iconphoto', window._w, icon)

        except TclError:
            print("Failed to open icon")

        #
        # Create initial graphs
        self.graphs = TabManager(window)
        for i in range(2): self.graphs.add()

        #
        # Menu Making

        self.menu_bar = Menu(window, fg="#66AA33")

        self.menu_bar.add_command(label='Pick a file', command=self.pick_graphing_file)

        self.menu_bar.add_command(label="Add new graph", command=self.graphs.add)
        self.menu_bar.add_command(label="Delete Last Graph", command=self.graphs.delete)

        self.menu_bar.add_command(label="Pull old config")

        self.menu_bar.add_command(label="Reset Selections")

        self.menu_bar.add_command(label="Save", command=self.save)

        self.menu_bar.add_checkbutton(label="Share tab settings", command=self.graphs.share_settings)

        #
        # Display window
        window.config(menu=self.menu_bar)
        window.mainloop()

    def pick_graphing_file(self):
        # # TODO - How to save this data?
        # # TODO - Make data get read and used

        self.data_file = filedialog.askopenfilename(
            title="Select file to Graph", filetypes=(("csv files", "*.csv"), ("all files", "*.*"))
        )

    def save(self, section=None):
        write_config(GUI.settings_file, self.graphs.get_data(tab_id=section))


if __name__ == "__main__":
    myClass = GUI()
