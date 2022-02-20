import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog as sd

import numpy as np

from ..functions import dp, pdd
from ..resources.language import Text
from .profile import ProfileHandler


class Measurement:
    def __init__(self, filepath, parent):

        self.filepath = filepath
        self.parent = parent
        self.filename = self.filepath.split("/")[-1][:-4]

        self.direction = self.parent.direction

        if self.parent.direction == None:
            dialog = GetType(self, self.parent)
            self.parent.parent.wait_window(dialog.top)

        if filepath.endswith(".txt"):
            data = np.loadtxt(self.filepath, unpack=True)
        else:
            data = np.genfromtxt(self.filepath, delimiter=",", unpack=True)

        self.axis, self.dose = data[0], data[1]
        self.normpoint = max(self.dose)

        try:
            self.std_dev = data[2]
        except IndexError:
            self.std_dev = []

        self.axis = self.axis.tolist()

        self.axis = {True: self.axis[len(self.axis) // 2 :], False: self.axis}
        self.dose = {True: self.dose[len(self.dose) // 2 :], False: self.dose}
        if self.std_dev != None:
            self.std_dev = self.std_dev = {
                True: self.std_dev[len(self.std_dev) // 2 :],
                False: self.std_dev,
            }

        else:
            self.std_dev = {
                True: self.std_dev,
                False: self.std_dev,
            }

    def params(self):
        if self.direction == "Z":
            return pdd.calculate_parameters(
                np.array(self.axis[False]),
                self.dose[False] / max(self.dose[False]),
                [],
            )
        else:
            params = dp.calculate_parameters(
                self.axis[False], self.dose[False] / max(self.dose[False])
            )
            self.cax = params[1]
            return params


class GetType:
    def __init__(self, measurement, parent):

        self.measurement = measurement
        self.parent = parent
        self.top = tk.Toplevel()
        self.geometry = [
            self.parent.parent.winfo_rootx(),
            self.parent.parent.winfo_rooty(),
            self.parent.winfo_width(),
            self.parent.winfo_height(),
        ]
        self.top.geometry(
            f"300x35+{self.parent.winfo_rootx()}+{self.parent.parent.winfo_rooty()}"
        )
        self.top.overrideredirect(1)

        self.xbutton = ttk.Button(self.top, text="X", command=self.x)
        self.ybutton = ttk.Button(self.top, text="Y", command=self.y)
        self.zbutton = ttk.Button(self.top, text="Z", command=self.z)

        self.xbutton.grid(column=0, row=0, padx=(5, 0))
        self.ybutton.grid(column=1, row=0, padx=(5, 5))
        self.zbutton.grid(column=2, row=0, padx=(0, 5))
        self.lift()

    def lift(self):
        self.new_geometry = [
            self.parent.parent.winfo_rootx(),
            self.parent.parent.winfo_rooty(),
            self.parent.winfo_width(),
            self.parent.winfo_height(),
        ]

        self.top.lift()
        self.top.after(100, self.lift)
        if self.new_geometry == self.geometry:
            return

        self.geometry = self.new_geometry
        self.top.geometry(
            f"300x35+{self.parent.winfo_rootx()}+{self.parent.parent.winfo_rooty()}"
        )

    def x(self):
        self.measurement.direction = "X"
        self.top.destroy()

    def y(self):
        self.measurement.direction = "Y"
        self.top.destroy()

    def z(self):
        self.measurement.direction = "Z"
        self.top.destroy()
