from tkinter import simpledialog as sd

import numpy as np
import topas2numpy

from ..classes.profile import ProfileHandler
from ..resources.language import Text


def load(path: str, normalize: bool):

    """
    A function that reads the relevant data from a TOPAS simulation
    output file in ASCII format. Determines the type of data (depth
    dose or dose profile) and calculates the standard deviation.
    Uses the binning information to create the proper directional 
    scaling and normalizes the maximum of the data to 1.
    """

    def norm(normalize, dose, std_dev):
        if normalize == True:
            std_dev = std_dev / max(dose)
            dose = dose / max(dose)

        return dose.flatten(), std_dev.flatten()

    def convert_SI(val, unit_in):
        SI = {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0}
        return val * SI[unit_in] / SI["mm"]

    data = topas2numpy.BinnedResult(path)
    bins = [dim.n_bins for dim in data.dimensions]
    if bins.count(1) != 2:
        print("Unsupported Experiment Type!")
        return
    axdict = {0: "X", 1: "Y", 2: "Z"}
    databin_index = bins.index(max(bins))
    direction = axdict[databin_index]
    axis = np.array(data.dimensions[databin_index].get_bin_centers())
    unit = data.dimensions[databin_index].unit
    if direction == "Z":
        axis = np.flip(axis)
    axis = [convert_SI(x, unit) for x in axis]
    scored_quantity = [i for i, j in zip(data.statistics, ["Sum", "Mean"]) if i == j][0]
    dose = data.data[scored_quantity]
    dose = dose.flatten()

    try:
        std_dev = data.data["Standard_Deviation"].flatten()
        histories = int(data.data["Histories_with_Scorer_Active"].flatten()[0])
        std_dev = std_dev * np.sqrt(histories)
    except KeyError as e:
        if e.args[0] == "Histories_with_Scorer_Active":
            lang = ProfileHandler().get_attribute("language")
            histories = sd.askinteger(title="  ", prompt=Text().histnum[lang])
            std_dev = data.data["Standard_Deviation"].flatten()

            std_dev = std_dev * np.sqrt(histories)
        else:
            std_dev = np.array([])

    dose, std_dev = norm(normalize, dose, std_dev)

    return axis, direction, dose, std_dev
