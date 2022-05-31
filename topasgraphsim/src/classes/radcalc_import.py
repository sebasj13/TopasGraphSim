import tkinter as tk
import tkinter.ttk as ttk

import numpy as np

from ..functions import dp, pdd
from ..resources.language import Text
from .measurement_import import GetType


class RadCalc:
    def __init__(self, filepath, parent):

        self.filepath = filepath
        self.parent = parent
        self.filename = self.filepath.split("/")[-1][:-4]

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

        self.axis, self.dose = np.array([i * 10 for i in data[0]]), data[2]  # cm to mm
        self.normpoint = max(self.dose)
        self.std_dev = []

        self.axis = self.axis.tolist()

        self.axis = {True: self.axis[len(self.axis) // 2 :], False: self.axis}
        self.dose = {True: self.dose[len(self.dose) // 2 :], False: self.dose}
        if self.std_dev != None:
            self.std_dev = self.std_dev = {
                True: self.std_dev[len(self.std_dev) // 2 :],
                False: self.std_dev,
            }

        else:
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
