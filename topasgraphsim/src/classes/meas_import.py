import numpy as np
import customtkinter as ctk

from .tgs_graph import TGS_Plot
from .paramframe import Parameters
from ..functions import pdd, dp
from ..resources.language import Text
from .profile import ProfileHandler
from .scrollframe import ScrollFrame

class TXTMeasurement:
    def __init__(self, path, direction, data, meas_type):

        self.filename = path.split("/")[-1][:-4]
        self.direction = direction
        self.data = data
        self.axis = self.data[:,0]

        if meas_type == "slicer":
            self.dose = self.data[:,2]
            self.std_dev = np.array([0.0 for i in range(len(self.dose))])
        else:
            self.dose = self.data[:,1]
            try: self.std_dev = self.data[:,2]
            except Exception: self.std_dev = np.array([0.0 for i in range(len(self.dose))])
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
        
        
class TXTImporter(ScrollFrame):
    def __init__(self, filepath, parent, plotlist, options, meas_type, delimiter, skiprows=0):
        super().__init__(parent=parent)
        try: self.data = np.loadtxt(filepath, delimiter=delimiter, skiprows=skiprows)
        except Exception:
            self.bell()
            return
        self.meas_type = meas_type
        self.text = Text()
        self.lang = ProfileHandler().get_attribute("language")
        self.plotlist = plotlist
        self.path = filepath
        self.options = options
        self.root = self.options.parent.master.master.parent
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.canvas.pack_propagate(False)
        theme = ProfileHandler().get_attribute("color_scheme")
        colors2 = {"light": "#E5E5E5", "dark":"#212121"}
        colors3 = {"light": "#DBDBDB", "dark":"#2B2B2B"}
        self.configure(fg_color=colors2[theme])
        self.canvas.configure(bg=colors3[theme], highlightbackground=colors3[theme])
        self.scrollbar.configure(fg_color=colors3[theme])
        self.options.dataframe2.grid_remove()
        self.options.dataframe1.grid_remove()
        self.grid(row=0, rowspan=2, column=0, sticky="nsew")
        self.label = ctk.CTkLabel(self.viewPort, text=Text().direction[self.lang], font=("Bahnschrift", 14, "bold"))
        self.label.pack(anchor="n", pady=5)
        directions = ["X", "Y", "Z"]
        self.direction = ctk.StringVar()
        self.directions = [ctk.CTkRadioButton(self.viewPort, text=direction, variable=self.direction, value=direction) for direction in directions]
        [button.pack(anchor="w", pady=5) for button in self.directions]
        self.submitbutton = ctk.CTkButton(
            self.viewPort,
            text=Text().submit[ProfileHandler().get_attribute("language")],
            command=self.submit,
        )
        self.submitbutton.pack(anchor="s", pady=5)
        
    def submit(self):
        
        self.plotlist += [TGS_Plot(self.options, TXTMeasurement(self.path, self.direction.get(), self.data, self.meas_type))]
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