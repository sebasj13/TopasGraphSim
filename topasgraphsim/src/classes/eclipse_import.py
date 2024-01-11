import customtkinter as ctk

import numpy as np

from ..functions import dp, pdd
from .profile import ProfileHandler
from .tgs_graph import TGS_Plot
from .paramframe import Parameters

class Eclipse:
    def __init__(self, filepath, parent, plotlist, options):

        self.filepath = filepath
        self.parent = parent
        self.lang = ProfileHandler().get_attribute("language")
        if "/" in self.filepath:
            self.filename = self.filepath.split("/")[-1][:-5]
        else:
            self.filename = self.filepath.split("\\")[-1][:-5]

        with open(filepath, "r") as f:
            l = f.readlines()
            data = l[12:-1]
            head = l[12]

        self.dose, self.axis = [], []
        for i,line in enumerate(data):
            points = line.replace(">","").replace("<","").strip().split(" ")
            self.axis += [float(points[0])]
            self.dose += [float(points[1])]

        self.dose = np.array(self.dose)
        self.axis = np.array(self.axis)

        self.direction = ""
        for line in head:
            if "Transversal" in line:
                self.direction = "Y"
            elif "Axial" in line:
                self.direction = "Z"
            
        if self.direction == "":
            self.direction = "X"

        self.std_dev = np.array([0 for i in range(len(self.dose))])

        plotlist += [TGS_Plot(options, self)]
        options.parameters.append(Parameters(options.paramslist.viewPort, plotlist[-1], self.lang))
        options.parameters[-1].grid(row=len(options.parameters)-1, sticky="ew", padx=5, pady=5)
        options.plotbuttons.append(ctk.CTkRadioButton(options.graphlist.viewPort, text=plotlist[-1].label, variable=options.current_plot, text_color = plotlist[-1].linecolor, value=plotlist[-1].label, command=options.change_current_plot, font=("Bahnschrift", 14, "bold")))
        options.plotbuttons[-1].grid(sticky="w", padx=5, pady=5)
        options.filenames.append(self.filepath)
        if len(options.parent.plots) == 1:
            options.enable_all_buttons()
            
        try:
            options.current_plot.set(plotlist[-1].label)
            options.parent.saved = False
            options.update_plotlist()
            options.parent.update()
        except IndexError:
            pass

    def params(self):
        if self.direction == "Z":
            return pdd.calculate_parameters(
                np.array(self.axis),
                self.dose / max(self.dose),
                [],
            )
        else:
            params = dp.calculate_parameters(
                self.axis, self.dose / max(self.dose))
            self.cax = params[1]
            return params
