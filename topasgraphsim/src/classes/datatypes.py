from tkinter import simpledialog as sd

import numpy as np
import topas2numpy

from ..functions import dp, pdd
from ..resources.language import Text
from .profile import ProfileHandler


class Measurement:
    def __init__(self, filepath, type):

        self.filepath = filepath
        self.filename = self.filepath.split("/")[-1]

        if type == "pdd":
            self.direction = "Z"
        else:
            self.direction = "X- {} Y".format(
                Text().orr[ProfileHandler().get_attribute("language")]
            )

        if filepath.endswith(".txt"):
            data = np.loadtxt(self.filepath, unpack=True)
        else:
            data = np.genfromtxt(self.filepath, delimiter=",", unpack=True)

        self.axis, self.dose = data[0], data[1]
        maximum = max(self.dose)
        self.norm_dose = np.array([value / maximum for value in self.dose])

        try:
            self.std_dev = data[2]
            self.norm_std_dev = self.std_dev / maximum
        except IndexError:
            self.std_dev = None
            self.norm_std_dev = None

        if self.direction == "Z":
            self.params = pdd.calculate_parameters(self.axis, self.dose, self.std_dev)
        else:
            self.params = dp.calculate_parameters(self.axis, self.dose, self.std_dev)


class Simulation:
    def __init__(self, filepath):

        self.filepath = filepath
        self.filename = self.filepath.split("/")[-1]

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
        if self.direction == "Z":
            self.axis = np.flip(self.axis)
        self.axis = [self.convert_SI(x, unit) for x in self.axis]
        scored_quantity = [
            i for i, j in zip(self.data.statistics, ["Sum", "Mean"]) if i == j
        ][0]

        self.dose = self.data.data[scored_quantity]
        self.dose = self.dose.flatten()

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

                self.std_dev = self.std_dev * np.sqrt(self.histories)
            else:
                std_dev = np.array([])
        self.norm_std_dev = self.std_dev / max(self.dose)
        self.norm_dose = self.dose / max(self.dose)

        if self.direction == "Z":
            self.params = pdd.calculate_parameters(self.axis, self.dose, self.std_dev)
        else:
            self.params = dp.calculate_parameters(self.axis, self.dose, self.std_dev)

    def convert_SI(self, val, unit_in):
        SI = {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0}
        return val * SI[unit_in] / SI["mm"]
