import customtkinter as ctk

import numpy as np

from ..functions import dp, pdd
from .profile import ProfileHandler
from .tgs_graph import TGS_Plot
from .paramframe import Parameters
from .measurement_import import GetType

class Slicer:
    def __init__(self, filepath, parent, plotlist, options):

        self.filepath = filepath
        self.parent = parent
        self.lang = ProfileHandler().get_attribute("language")
        if "/" in self.filepath:
            self.filename = self.filepath.split("/")[-1][:-4]
        else:
            self.filename = self.filepath.split("\\")[-1][:-4]

        data = np.loadtxt(self.filepath, delimiter="\t", skiprows=1, unpack=True)

        dialog = GetType(self, self.parent, "")
        self.parent.parent.wait_window(dialog.top)

        self.axis, self.dose = np.array(data[0]), np.array(data[2])
        self.std_dev = np.array([0 for i in range(len(self.dose))])

        plotlist += [TGS_Plot(options, self)]
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
