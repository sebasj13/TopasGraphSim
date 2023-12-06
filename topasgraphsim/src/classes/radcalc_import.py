import customtkinter as ctk

import numpy as np

from ..functions import dp, pdd
from ..resources.language import Text
from .profile import ProfileHandler
from .measurement_import import GetType
from .tgs_graph import TGS_Plot
from .paramframe import Parameters

class RadCalcData:
    def __init__(self, filename, axis, dose, std_dev, direction):
        
        self.filename = filename
        self.axis = axis
        self.dose = dose
        self.std_dev = std_dev
        self.direction = direction
        self.normpoint = max(self.dose)
        
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


class RadCalc:
    def __init__(self, filepath, parent, plotlist, options):

        self.filepath = filepath
        self.parent = parent
        self.lang = ProfileHandler().get_attribute("language")
        if "/" in self.filepath:
            self.filename = self.filepath.split("/")[-1][:-4]
        else:
            self.filename = self.filepath.split("\\")[-1][:-4]

        data = np.loadtxt(self.filepath, delimiter=",", skiprows=11, unpack=True)
        with open(self.filepath) as file:
            head = [next(file) for x in range(11)]

        for line in head:
            if "Inplane" in line:
                self.direction = "X"
            elif "Crossplane" in line:
                self.direction = "Y"
            elif "PDD" in line:
                self.direction = "Z"

        self.axis, self.mdose, self.cdose = np.array([i * 10 for i in data[0]]), np.array(data[1]), np.array(data[2])  # cm to mm
        self.std_dev = np.array([0 for i in range(len(self.cdose))])
        
        data = [RadCalcData("Measured_"+self.filename, self.axis, self.mdose, self.std_dev, self.direction),
                RadCalcData("Computed_"+self.filename, self.axis, self.cdose, self.std_dev, self.direction)]
        
        for d in data:
            plotlist += [TGS_Plot(options, d)]
            options.parameters.append(Parameters(options.paramslist.viewPort, plotlist[-1], self.lang))
            options.parameters[-1].grid(row=len(options.parameters)-1, sticky="ew", padx=5, pady=5)
            options.plotbuttons.append(ctk.CTkRadioButton(options.graphlist.viewPort, text=plotlist[-1].label, variable=options.current_plot, text_color = plotlist[-1].linecolor, value=plotlist[-1].label, command=options.change_current_plot, font=("Bahnschrift", 14, "bold")))
            options.plotbuttons[-1].grid(sticky="w", padx=5, pady=5)
            if len(options.parent.plots) == 1:
                options.enable_all_buttons()
            
        try:
            options.current_plot.set(plotlist[-1].label)
            options.filenames.append(self.filepath)
            options.parent.saved = False
            options.update_plotlist()
            options.parent.update()
        except IndexError:
            pass
