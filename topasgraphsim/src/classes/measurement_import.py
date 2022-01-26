import numpy as np

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
        if self.direction != "Z":
            self.axis = np.array(
                [x - (max(self.axis) + min(self.axis)) / 2 for x in self.axis]
            )
        maximum = max(self.dose)
        self.norm_dose = np.array([value / maximum for value in self.dose])

        try:
            self.std_dev = data[2]
            self.norm_std_dev = self.std_dev / maximum
        except IndexError:
            self.std_dev = None
            self.norm_std_dev = None

        if self.direction == "Z":
            self.params = pdd.calculate_parameters(
                self.axis, self.norm_dose, self.norm_std_dev
            )
        else:
            self.params = dp.calculate_parameters(
                self.axis, self.norm_dose, self.norm_std_dev
            )
        self.axis = self.axis.tolist()

        self.axis = {True: self.axis[len(self.axis) // 2 :], False: self.axis}
        self.dose = {
            True: {
                True: self.norm_dose[len(self.norm_dose) // 2 :],
                False: self.dose[len(self.dose) // 2 :],
            },
            False: {True: self.norm_dose, False: self.dose},
        }
        self.std_dev = {
            True: {
                True: self.norm_std_dev[len(self.norm_std_dev) // 2 :],
                False: self.std_dev[len(self.std_dev) // 2 :],
            },
            False: {True: self.norm_std_dev, False: self.std_dev},
        }
