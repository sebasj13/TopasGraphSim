import os
import tkinter as tk
from collections import deque

from matplotlib.pyplot import axes

from ..resources.language import Text
from .profile import ProfileHandler


class RecentFileManager:
    def __init__(self, parent):

        self.parent = parent

        self.recent_files = self.parent.profile.get_attribute("recent_files")

        pop = []
        for i, x in enumerate([file[0] for file in self.recent_files]):
            if os.path.exists(x) != True:
                pop.append(i)

        for i in pop:
            self.recent_files.pop(i)

        self.lambdas = [
            lambda: self.add_recent_file_to_data(0),
            lambda: self.add_recent_file_to_data(1),
            lambda: self.add_recent_file_to_data(2),
            lambda: self.add_recent_file_to_data(3),
            lambda: self.add_recent_file_to_data(4),
        ]

    def add_file(self, file):

        if file[0] in [file[0] for file in self.recent_files]:
            self.recent_files.pop(
                [file[0] for file in self.recent_files].index(file[0])
            )
            self.recent_files.append(None)
            rotatable = deque(self.recent_files)
            rotatable.rotate(1)
            self.recent_files = list(rotatable)
            self.recent_files[0] = file
            self.parent.profile.set_attribute("recent_files", self.recent_files)

        elif len(self.recent_files) == 5:
            self.recent_files.pop(-1)
            self.recent_files.append(None)
            rotatable = deque(self.recent_files)
            rotatable.rotate(1)
            self.recent_files = list(rotatable)
            self.recent_files[0] = file
            self.parent.profile.set_attribute("recent_files", self.recent_files)

        else:
            self.recent_files.append(file)
            rotatable = deque(self.recent_files)
            rotatable.rotate(1)
            self.recent_files = list(rotatable)
            self.parent.profile.set_attribute("recent_files", self.recent_files)

    def add_recent_file_to_data(self, index):
        if self.recent_files[index][0] in [file[0] for file in self.parent.filenames]:
            return
        if os.path.exists(self.recent_files[index][0]) == True:

            self.parent.load_dropped_file("{" + self.recent_files[index][0] + "}")
            self.add_files_to_menu()

        else:
            self.recent_files.pop(index)
            self.recentmenu.delete(index)

    def add_files_to_menu(self):
        try:
            self.recentmenu.destroy()
        except AttributeError:
            pass

        self.recentmenu = tk.Menu(self.parent.menubar, tearoff=False)

        if len(self.recent_files) == 0:
            self.recentmenu.add_command(label="---")
            self.recentmenu.entryconfig(0, state=tk.DISABLED)

        else:

            for index, file in enumerate(self.recent_files):

                self.recentmenu.add_command(
                    label=os.path.basename(file[0]), command=self.lambdas[index]
                )

        self.parent.filemenu.insert_cascade(
            2,
            label=Text().recent[ProfileHandler().get_attribute("language")],
            menu=self.recentmenu,
        )
        self.parent.filemenu.delete(3)

