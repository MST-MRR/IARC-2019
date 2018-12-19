from tkinter import Tk, Menu, PhotoImage, TclError, filedialog

from tools.old_gui.tab_manager import TabManager

from tools.file_oi.file_io import write_config


# Future
# TODO - Make clear what data each tool needs

# TODO - Implement scrolled frame

# TODO - pull old settings into window <- function that share data setting uses also to parse out relevant parts

# TODO - Finish menu

# TODO - Fix file_io problems based on where program is called from
# TODO - File_io detect where program is being called from and add necessary directories

# TODO - Tab configurations to set names, disable parts for each

# TODO - Should save function be put in tab manager

# TODO - Add all configuration stuff here

# TODO - Tell tabmanager what tabs to be created and their configurations

# TODO - All data should have a standard structure to which it can be sent to the file_io and encoded and decoded
# TODO - GUI manages menu, tab and color configurations and initializations
# TODO - Handles interactions with other tools ie fileio
# TODO - Parent directory should be found here and sent to other classes


class GUI:
    """
    GUI to edit and create config files for all tools.
    """

    icon_file = '../../ninja_icon.gif'

    def __init__(self):
        # Window setup
        self.window = Tk()
        self.window.title("Multirotor Robot Data Graphing Tool")
        self.window.geometry('750x500')
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        try:
            icon = PhotoImage(file=GUI.icon_file)
            self.window.tk.call('wm', 'iconphoto', self.window._w, icon)

        except TclError:
            print("Failed to open icon")

        # Tabs
        self.graph_manager = TabManager(self.window)
        self.graph_manager.add_graph()

        # Top Menu
        self.menu_bar = Menu(self.window, fg="#66AA33")
        self.window.config(menu=self.menu_bar)

        # TODO - self.menu_bar.add_command(label='Pick a file', command=self.graphs.pick_graphing_file)

        self.menu_bar.add_command(label="Add new graph", command=self.graph_manager.add_graph)
        self.menu_bar.add_command(label="Delete Last Graph", command=self.graph_manager.delete_graph)

        # TODO - self.menu_bar.add_command(label="Pull old config")

        self.menu_bar.add_command(label="Save", command=self.save)

        # TODO - self.menu_bar.add_checkbutton(label="Share tab settings", command=self.graphs.share_settings)

        # Display window
        self.window.mainloop()

    def close_window(self):
        """
        A custom close function.
        """

        self.window.destroy()

    def save(self, section=None):
        """
        Save tab data into config file.

        Parameters
        ----------
        section: number, default=None
            Tab index to save, if not default use current tab.
        """

        filename = filedialog.asksaveasfilename(
            title="Save config as...", defaultextension=".xml", filetypes=(("xml file", "*.xml"),("All Files", "*.*")))

        if filename:
            write_config(filename, self.graph_manager.get_graph_data(tab_id=section))


if __name__ == "__main__":
    myClass = GUI()
