import os
import re
import customtkinter as ctk

import numpy as np

from ..functions import dp, pdd
from ..resources.language import Text
from .profile import ProfileHandler
from .tgs_graph import TGS_Plot
from .paramframe import Parameters
from .scrollframe import ScrollFrame

class PTWMeasurement:
    def __init__(self, list, index):

        self.axis = np.array(list[0])
        self.dose = np.array(list[1])
        self.direction = list[4]
        self.normpoint = max(self.dose)

        self.std_dev = np.array([0.0 for i in range(len(self.dose))])

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


class PTWMultimporter(ScrollFrame):
    def __init__(self, filepath, parent, plotlist, options):
        super().__init__(parent=parent)
        self.parent = parent
        self.text = Text()
        self.lang = ProfileHandler().get_attribute("language")
        self.plotlist = plotlist
        self.path = filepath
        self.options = options
        self.root = self.options.parent.master.master.parent
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.canvas.pack_propagate(False)
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
                    axes["INPLANE_PROFILE"] = line.split("=")[-1].strip()
                elif (
                    bool(
                        re.match(
                            re.compile(r"^CROSSPLANE_AXIS$"), line.split("=")[0].strip()
                        )
                    )
                    == True
                ):
                    axes["CROSSPLANE_PROFILE"] = line.split("=")[-1].strip()
                elif (
                    bool(
                        re.match(
                            re.compile(r"^DEPTH_AXIS$"), line.split("=")[0].strip()
                        )
                    )
                    == True
                ):
                    axes["PDD"] = line.split("=")[-1].strip()

                elif "SCAN_CURVETYPE" in line:
                    direction = axes[line.split("=")[-1][:-1]]
                    if direction not in "xyzXYZ":
                        rev_axes = {v: k for k, v in axes.items()}
                        direcs = {"INPLANE_PROFILE":"X", "CROSSPLANE_PROFILE":"Y", "PDD":"Z"}
                        
                        direction = direcs[rev_axes[direction]]

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
        theme = ProfileHandler().get_attribute("color_scheme")
        colors2 = {"light": "#E5E5E5", "dark":"#212121"}
        colors3 = {"light": "#DBDBDB", "dark":"#2B2B2B"}
        self.configure(fg_color=colors2[theme])
        self.canvas.configure(bg=colors3[theme], highlightbackground=colors3[theme])
        self.scrollbar.configure(fg_color=colors3[theme])
        self.options.dataframe2.grid_remove()
        self.options.dataframe1.grid_remove()
        self.grid(row=0, rowspan=2, column=0, sticky="nsew")
        self.label = ctk.CTkLabel(self.viewPort, text=Text().select[self.lang], font=("Bahnschrift", 14, "bold"))
        self.label.pack(anchor="n", pady=5)
        self.variables = [ctk.BooleanVar() for i in range(len(self.alldata))]
        [var.set(False) for var in self.variables]
        textdict = {
            "X": f"{self.text.dp[self.lang]}" + " X",
            "Y": f"{self.text.dp[self.lang]}" + " Y",
            "Z": f"{self.text.pdd[self.lang]}",
        }
        self.buttons = [
            ctk.CTkCheckBox(
                self.viewPort,
                variable=self.variables[i],
                text=f"Scan {i+1}: {textdict[PTWMeasurement(self.alldata[i], i+1).direction.upper()]}",
            )
            for i in range(len(self.alldata))
        ]
        [button.pack(anchor="w") for button in self.buttons]
        self.submitbutton = ctk.CTkButton(
            self.viewPort,
            text=Text().submit[ProfileHandler().get_attribute("language")],
            command=self.submit,
        )
        self.submitbutton.pack(anchor="s", pady=5)
        self.parent.master.master.parent.bind("<Return>", self.submit)

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
        try:
            self.options.current_plot.set(self.plotlist[-1].label)
            self.options.filenames.append(self.path)
            self.options.parent.saved = False
            self.options.update_plotlist()
            self.options.parent.update()
        except IndexError:
            pass
        
        self.canvas.unbind_all("<MouseWheel>")
        self.destroy()
        self.options.dataframe1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.options.dataframe2.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
