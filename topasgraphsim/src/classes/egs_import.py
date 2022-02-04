from tkinter import simpledialog as sd

import numpy as np
import topas2numpy

from ..functions import dp, pdd
from ..resources.language import Text
from .profile import ProfileHandler


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
