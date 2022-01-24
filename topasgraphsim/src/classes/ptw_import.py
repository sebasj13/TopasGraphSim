import os
import tkinter as tk
import tkinter.ttk as ttk

import numpy as np

from ..functions import dp, pdd
from ..resources.language import Text
from .profile import ProfileHandler


class PTWMeasurement:
    def __init__(self, list, index):

        self.axis = list[0]
        self.dose = list[1]
        if self.axis[0] < 0:
            self.direction = "X- {} Y".format(
                Text().orr[ProfileHandler().get_attribute("language")]
            )
        else:
            self.direction = "Z"
        maximum = max(self.dose)
        self.norm_dose = np.array([value / maximum for value in self.dose])

        self.std_dev = None
        self.norm_std_dev = None

        if self.direction == "Z":
            self.params = pdd.calculate_parameters(
                self.axis, self.norm_dose, self.norm_std_dev
            )
        else:
            self.params = dp.calculate_parameters(
                self.axis, self.norm_dose, self.norm_std_dev
            )
        self.filename = f"PTW Scan {index}"
        self.filepath = list[2]
        self.unit = list[3]


class PTWMultimporter:
    def __init__(self, filepath, geometry):

        with open(filepath, "r") as file:
            lines = file.readlines()
            unit = str
            self.alldata = []
            for index, line in enumerate(lines):
                if "MEAS_UNIT" in line:
                    unit = line.split("=")[-1]
                if "BEGIN_DATA" in line:
                    xdata, ydata = [], []
                    i = 1
                    while "END_DATA" not in lines[index + i]:
                        xdata += [float(lines[index + i].split("\t")[3])]
                        ydata += [float(lines[index + i].split("\t")[5])]
                        i += 1
                    self.alldata += [[np.array(xdata), np.array(ydata), filepath, unit]]
                    unit = str

        self.plots = []

        self.window = tk.Toplevel()
        self.window.wm_attributes("-toolwindow", True)
        self.window.title("PTW tbaScan")
        self.window.resizable(False, False)
        self.window.bind("<Return>", self.submit)
        self.geometry = [
            geometry.winfo_rootx(),
            geometry.winfo_rooty(),
            geometry.winfo_height(),
        ]
        self.height = 29 * (len(self.alldata) + 1)
        self.window.geometry(
            f"120x{self.height}+{self.geometry[0]}+{25+(self.geometry[0]+self.geometry[2])//2-self.height//2}"
        )
        self.window.iconbitmap(
            str(
                os.path.dirname(os.path.realpath(__file__))
                + "\\..\\resources\\icon.ico"
            )
        )
        self.frame = tk.Frame(self.window)
        self.frame.pack()
        self.variables = [tk.BooleanVar() for i in range(len(self.alldata))]
        [var.set(False) for var in self.variables]
        self.buttons = [
            ttk.Checkbutton(self.frame, variable=self.variables[i], text=f"Scan {i+1}",)
            for i in range(len(self.alldata))
        ]
        [button.grid() for button in self.buttons]
        self.submitbutton = ttk.Button(
            self.frame,
            text=Text().submit[ProfileHandler().get_attribute("language")],
            command=self.submit,
        )
        self.submitbutton.grid()

    def submit(self, event=None):

        self.plots = []

        for index, dataset in enumerate(self.alldata):
            if self.variables[index].get() == True:
                self.plots += [PTWMeasurement(dataset, index + 1)]
                if len(self.variables) == 5:
                    break

            self.window.quit()