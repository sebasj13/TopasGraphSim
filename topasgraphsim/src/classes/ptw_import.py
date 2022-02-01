import os
import re
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
        self.direction = list[4]
        self.normpoint = max(self.dose)

        self.std_dev = []

        self.axis = self.axis.tolist()
        self.filepath = list[2]
        self.filename = self.filepath.split("/")[-1][:-4] + f" - Scan {index}"
        self.unit = list[3]

        self.axis = {True: self.axis[len(self.axis) // 2 :], False: self.axis}
        self.dose = {True: self.dose[len(self.dose) // 2 :], False: self.dose}
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


class PTWMultimporter:
    def __init__(self, filepath, geometry):

        self.text = Text()
        self.lang = ProfileHandler().get_attribute("language")
        self.main_viewer = geometry

        with open(filepath, "r") as file:
            lines = file.readlines()
            unit = ""
            self.alldata = []
            axes = {}
            direction = ""
            for index, line in enumerate(lines):
                if "MEAS_UNIT" in line:
                    unit = line.split("=")[-1]

                elif (
                    bool(
                        re.match(
                            re.compile(r"^INPLANE_AXIS$"), line.split("=")[0].strip()
                        )
                    )
                    == True
                ):
                    axes["INPLANE_PROFILE"] = line.split("=")[-1][0]
                elif (
                    bool(
                        re.match(
                            re.compile(r"^CROSSPLANE_AXIS$"), line.split("=")[0].strip()
                        )
                    )
                    == True
                ):
                    axes["CROSSPLANE_PROFILE"] = line.split("=")[-1][0]
                elif (
                    bool(
                        re.match(
                            re.compile(r"^DEPTH_AXIS$"), line.split("=")[0].strip()
                        )
                    )
                    == True
                ):
                    axes["PDD"] = line.split("=")[-1][0]

                elif "SCAN_CURVETYPE" in line:
                    direction = axes[line.split("=")[-1][:-1]]

                if "BEGIN_DATA" in line:
                    xdata, ydata = [], []
                    i = 1
                    while "END_DATA" not in lines[index + i]:
                        xdata += [float(lines[index + i].split("\t")[3])]
                        ydata += [float(lines[index + i].split("\t")[5])]
                        i += 1
                    self.alldata += [
                        [np.array(xdata), np.array(ydata), filepath, unit, direction]
                    ]
                    unit = ""
                    direction = ""
                    axes = {}

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
            f"240x{self.height}+{self.geometry[0]}+{25+(self.geometry[0]+self.geometry[2])//2-self.height//2}"
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
        textdict = {
            "X": f"{self.text.dp[self.lang]}" + " X",
            "Y": f"{self.text.dp[self.lang]}" + " Y",
            "Z": f"{self.text.pdd[self.lang]}",
        }
        self.buttons = [
            ttk.Checkbutton(
                self.frame,
                variable=self.variables[i],
                text=f"Scan {i+1}: {textdict[PTWMeasurement(self.alldata[i], i+1).direction]}",
            )
            for i in range(len(self.alldata))
        ]
        [button.grid(sticky="W") for button in self.buttons]
        self.submitbutton = ttk.Button(
            self.frame,
            text=Text().submit[ProfileHandler().get_attribute("language")],
            command=self.submit,
        )
        self.submitbutton.grid(sticky="S")
        self.window.protocol("WM_DELETE_WINDOW", self.close)

    def close(self):
        self.plots = []
        self.main_viewer.filenames.pop(-1)
        self.window.destroy()

    def submit(self, event=None):

        self.plots = []

        for index, dataset in enumerate(self.alldata):
            if self.variables[index].get() == True:
                self.plots += [PTWMeasurement(dataset, index + 1)]

                if len(self.variables) == 5:
                    break

            self.window.quit()
