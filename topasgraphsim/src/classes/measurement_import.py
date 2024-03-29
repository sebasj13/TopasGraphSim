import tkinter as tk
import tkinter.ttk as ttk

import numpy as np

from ..functions import dp, pdd
from ..resources.language import Text


class Measurement:
    def __init__(self, filepath, parent):

        self.filepath = filepath
        self.parent = parent
    
        if "/" in self.filepath:
            self.filename = self.filepath.split("/")[-1][:-4]
        else:
            self.filename = self.filepath.split("\\")[-1][:-4]

        data = np.loadtxt(self.filepath, unpack=True)
        self.unit = ""
        self.axis, self.dose = np.array(data[0]), np.array(data[1])
        self.normpoint = max(self.dose)

        try:
            self.std_dev = np.array(data[2])
        except IndexError:
            self.std_dev = (np.array([0 for i in range(len(self.dose))]))

        dialog = GetType(self, self.parent, "")
        self.parent.parent.wait_window(dialog.top)

    def params(self):
        if self.direction == "Z":
            return pdd.calculate_parameters(
                np.array(self.axis),
                self.dose / max(self.dose),
                [],
            )
        else:
            params = dp.calculate_parameters(
                self.axis, self.dose[False] / max(self.dose)
            )
            self.cax = params[1]
            return params


class GetType:
    def __init__(self, measurement, parent, opt: str):

        self.measurement = measurement
        self.parent = parent
        self.top = tk.Toplevel()
        self.geometry = [
            self.parent.parent.winfo_rootx(),
            self.parent.parent.winfo_rooty(),
            self.parent.winfo_width(),
            self.parent.winfo_height(),
        ]
        self.width = 300
        if opt == "NoPDD":
            self.width = 200
        self.top.geometry(
            f"{self.width}x60+{self.parent.winfo_rootx()}+{self.parent.parent.winfo_rooty()}"
        )
        self.top.overrideredirect(1)

        self.xbutton = ttk.Button(self.top, text="X", command=self.x)
        self.ybutton = ttk.Button(self.top, text="Y", command=self.y)
        self.zbutton = ttk.Button(self.top, text="Z", command=self.z)
        self.dplabel = ttk.Label(self.top, text=Text().dp[self.parent.lang])
        self.pddlabel = ttk.Label(self.top, text=Text().pdd[self.parent.lang])

        self.dplabel.grid(row=0, column=0, columnspan=2, padx=(5, 5))
        self.xbutton.grid(column=0, row=1, padx=(5, 0))
        self.ybutton.grid(column=1, row=1, padx=(5, 5))
        if opt != "NoPDD":
            self.pddlabel.grid(row=0, column=2, padx=(0, 5))
            self.zbutton.grid(column=2, row=1, padx=(0, 5))
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
            f"{self.width}x60+{self.parent.winfo_rootx()}+{self.parent.parent.winfo_rooty()}"
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
