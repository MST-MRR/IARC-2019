from tkinter import Tk, Menu, PhotoImage, TclError, filedialog

from tools.config_maker.tab_manager import TabManager

from tools.file_io.file_io import write_config

# BASE WORKING
# TODO - Base working version to push, create separate branch for tools
# TODO - Add ipc to base working version
# TODO - Base working version include documentation & functionality for -> logger, csvgrapher, file_io and config maker
# TODO - Base working will have to have file_io issues fixed

# Future
# TODO - Make clear what data each tool needs

# TODO - Implement scrolled frame

# TODO - pull old settings into window <- function that share data setting uses also to parse out relevant parts

# TODO - Way to save what file you want graphed
# TODO - Chose where to save based on tab ! and set variable to set it

# TODO - Fix file_io problems based on where program is called from
# TODO - File_io detect where program is being called from and add necessary directories

# TODO - Finish menu

# TODO - Tab configurations to set names, disable parts for each

# TODO - Should save be put in tabs

# TODO - Add all configuration stuff here

# TODO - All data should have a standard structure to which it can be sent to the file_io and encoded and decoded
# TODO - GUI manages menu, tab and color configurations and initializations
# TODO - Handles interactions with other tools ie fileio
# TODO - Parent directory should be found here and sent to other classes

class GUI:
    """

    """

    icon_file = '../../ninja_icon.gif'

    def __init__(self):
        # Window setup
        window = Tk()
        window.title("Multirotor Robot Data Graphing Tool")
        window.geometry('750x500')

        try:
            icon = PhotoImage(file=GUI.icon_file)
            window.tk.call('wm', 'iconphoto', window._w, icon)

        except TclError:
            print("Failed to open icon")

        # Tabs
        self.graphs = TabManager(window)  # TODO - Tell tabmanager what tabs to be created and their configurations
        self.graphs.add()

        # Top Menu
        self.menu_bar = Menu(window, fg="#66AA33")
        window.config(menu=self.menu_bar)

        # TODO - self.menu_bar.add_command(label='Pick a file', command=self.graphs.pick_graphing_file)

        self.menu_bar.add_command(label="Add new graph", command=self.graphs.add)
        self.menu_bar.add_command(label="Delete Last Graph", command=self.graphs.delete)

        # TODO - self.menu_bar.add_command(label="Pull old config")

        self.menu_bar.add_command(label="Save", command=self.save)

        # TODO - self.menu_bar.add_checkbutton(label="Share tab settings", command=self.graphs.share_settings)

        # Display window
        window.mainloop()

    def save(self, section=None):
        filename = filedialog.asksaveasfilename(
            title="Save config as...", defaultextension=".xml", filetypes=(("xml file", "*.xml"),("All Files", "*.*")))

        if filename:
            write_config(filename, self.graphs.get_data(tab_id=section))


if __name__ == "__main__":
    myClass = GUI()
