from tkinter import simpledialog as sd

import numpy as np
import topas2numpy

from ..functions import dp, pdd
from ..resources.language import Text
from .profile import ProfileHandler


class Simulation:
    def __init__(self, filepath):

        self.filepath = filepath
        self.filename = self.filepath.split("/")[-1][:-4]

        self.data = topas2numpy.BinnedResult(self.filepath)
        bins = [dim.n_bins for dim in self.data.dimensions]
        if bins.count(1) != 2:
            print("Unsupported Experiment Type!")
            return

        axdict = {0: "X", 1: "Y", 2: "Z"}
        databin_index = bins.index(max(bins))
        self.direction = axdict[databin_index]
        self.axis = np.array(self.data.dimensions[databin_index].get_bin_centers())
        unit = self.data.dimensions[databin_index].unit
        self.axis = np.flip(self.axis)
        self.axis = [self.convert_SI(x, unit) for x in self.axis]
        if "Mean" in self.data.statistics:
            scored_quantity = "Mean"
        if "Sum" in self.data.statistics:
            scored_quantity = "Sum"
        self.dose = self.data.data[scored_quantity]
        self.dose = self.dose.flatten()
        self.unit = self.data.unit

        try:
            self.std_dev = self.data.data["Standard_Deviation"].flatten()
            self.histories = int(
                self.data.data["Histories_with_Scorer_Active"].flatten()[0]
            )
            self.std_dev = self.std_dev * np.sqrt(self.histories)
        except KeyError as e:
            if e.args[0] == "Histories_with_Scorer_Active":
                lang = ProfileHandler().get_attribute("language")
                self.histories = sd.askinteger(title="  ", prompt=Text().histnum[lang])
                self.std_dev = self.data.data["Standard_Deviation"].flatten()
                if scored_quantity == "Sum":
                    self.std_dev = self.std_dev * np.sqrt(self.histories)
                else:
                    self.std_dev = self.std_dev / np.sqrt(self.histories)
            else:
                std_dev = np.array([])

        if self.direction != "Z":
            self.axis = np.array(
                [x - (max(self.axis) + min(self.axis)) / 2 for x in self.axis]
            )
            self.axis = self.axis.tolist()

        self.normpoint = max(self.dose)
        self.axis = {True: self.axis[len(self.axis) // 2 :], False: self.axis}
        self.dose = {True: self.dose[len(self.dose) // 2 :], False: self.dose}
        self.std_dev = {
            True: self.std_dev[len(self.std_dev) // 2 :],
            False: self.std_dev,
        }

    def params(self):
        if self.direction == "Z":
            return pdd.calculate_parameters(
                self.axis[False],
                self.dose[False] / max(self.dose[False]),
                self.std_dev[False] / max(self.dose[False]),
            )
        else:
            params = dp.calculate_parameters(
                self.axis[False], self.dose[False] / max(self.dose[False])
            )
            self.cax = params[1]
            return params

    def convert_SI(self, val, unit_in):
        SI = {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0}
        return val * SI[unit_in] / SI["mm"]


class EGSSimulation:
    def __init__(self, filepath):

        self.filepath = filepath
        self.filename = self.filepath.split("/")[-1][:-7]

        self.direction = ""
        self.unit = ""
        self.dose = []
        self.std_dev = []
        self.axis = []

        self.axis = {True: self.axis[len(self.axis) // 2 :], False: self.axis}
        self.std_dev = {
            True: self.std_dev[len(self.std_dev) // 2 :],
            False: self.std_dev,
        }
        self.normpoint = max(self.dose)
