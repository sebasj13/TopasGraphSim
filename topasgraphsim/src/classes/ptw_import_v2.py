import os
import re
import customtkinter as ctk

import numpy as np

from ..functions import dp, pdd
from ..resources.language import Text
from .profile import ProfileHandler
from .tgs_graph_v2 import TGS_Plot
from .paramframe_v2 import Parameters


class PTWMeasurement:
    def __init__(self, list, index):

        self.axis = np.array(list[0])
        self.dose = np.array(list[1])
        self.direction = list[4]
        self.normpoint = max(self.dose)

        self.std_dev = []

        self.filepath = list[2]
        
        if "/" in self.filepath:
            self.filename = self.filepath.split("/")[-1][:-4] + f" - Scan {index}"
        else:
            self.filename = self.filepath.split("\\")[-1][:-4] + f" - Scan {index}"
        
        self.unit = list[3]


    def params(self):
        if self.direction == "Z":
            return pdd.calculate_parameters(
                np.array(self.axis),
                self.dose / max(self.dose),
                [],
            )
        else:
            params = dp.calculate_parameters(
                self.axis, self.dose / max(self.dose)
            )
            self.cax = params[1]
            return params


class PTWMultimporter:
    def __init__(self, filepath, plotlist, options):

        self.text = Text()
        self.lang = ProfileHandler().get_attribute("language")
        self.plotlist = plotlist
        self.path = filepath
        self.options = options
        self.root = self.options.parent.master.master.parent

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
                    if direction == "x":
                        direction = "X"
                    elif direction == "y":
                        direction = "Y"
                    elif direction == "z":
                        direction = "Z"

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
        self.window = ctk.CTkToplevel()
        # self.window.wm_attributes("-toolwindow", True)
        self.window.overrideredirect(1)
        self.window.title("PTW tbaScan")
        self.window.resizable(False, False)
        self.window.bind("<Return>", self.submit)
        self.geometry = [
            self.root.winfo_rootx(),
            self.root.winfo_rooty(),
            self.root.winfo_width(),
            self.root.winfo_height(),
        ]
        self.height = 10 + 29 * (len(self.alldata) + 1)
        self.width = 220
        if self.lang == "en":
            self.width = 180
        self.window.geometry(
            f"{self.width}x{self.height}+{self.root.winfo_rootx()}+{self.root.parent.winfo_rooty()}"
        )
        self.window.iconbitmap(
            str(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "..",
                    "resources",
                    "icon.ico",
                )
            )
        )
        self.frame = ctk.CTkFrame(self.window)
        self.frame.pack()
        self.variables = [ctk.BooleanVar() for i in range(len(self.alldata))]
        [var.set(False) for var in self.variables]
        textdict = {
            "X": f"{self.text.dp[self.lang]}" + " X",
            "x": f"{self.text.dp[self.lang]}" + " X",
            "Y": f"{self.text.dp[self.lang]}" + " Y",
            "y": f"{self.text.dp[self.lang]}" + " Y",
            "Z": f"{self.text.pdd[self.lang]}",
            "z": f"{self.text.pdd[self.lang]}",
        }
        self.buttons = [
            ctk.CTkCheckBox(
                self.frame,
                variable=self.variables[i],
                text=f"Scan {i+1}: {textdict[PTWMeasurement(self.alldata[i], i+1).direction]}",
            )
            for i in range(len(self.alldata))
        ]
        [button.grid(sticky="W") for button in self.buttons]
        self.submitbutton = ctk.CTkButton(
            self.frame,
            text=Text().submit[ProfileHandler().get_attribute("language")],
            command=self.submit,
        )
        self.submitbutton.grid(sticky="S")
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        self.lift()

    def lift(self):
        self.new_geometry = [
            self.root.winfo_rootx(),
            self.root.winfo_rooty(),
            self.root.winfo_width(),
            self.root.winfo_height(),
        ]

        self.window.lift()
        self.window.after(100, self.lift)
        if self.new_geometry == self.geometry:
            return

        self.geometry = self.new_geometry
        self.window.geometry(
            f"{self.width}x{self.height}+{self.root.winfo_rootx()}+{self.root.winfo_rooty()}"
        )

    def close(self):
        self.plots = []
        self.window.destroy()

    def submit(self, event=None):

        self.plots = []


        for index, dataset in enumerate(self.alldata):
            if self.variables[index].get() == True:
                self.plotlist += [TGS_Plot(self.options, PTWMeasurement(dataset, index + 1))]
                self.options.parameters.append(Parameters(self.options.paramslist.viewPort, self.plotlist[-1], self.lang))
                self.options.parameters[-1].grid(row=len(self.options.parameters)-1, sticky="ew", padx=5, pady=5)
                self.options.plotbuttons.append(ctk.CTkRadioButton(self.options.graphlist.viewPort, text=self.plotlist[-1].label, variable=self.options.current_plot, text_color = self.plotlist[-1].linecolor, value=self.plotlist[-1].label, command=self.options.change_current_plot, font=("Bahnschrift", 14, "bold")))
                self.options.plotbuttons[-1].grid(sticky="w", padx=5, pady=5)
            if len(self.options.parent.plots) == 1:
                self.options.enable_all_buttons()
                
        self.options.current_plot.set(self.plotlist[-1].label)
        self.options.filenames.append(self.path)
        self.options.parent.saved = False
        self.options.parent.update()
        self.window.destroy()
