from tkinter import simpledialog as sd
import numpy as np

from ..functions import dp, egspdd


class EGSSimulation:
    def __init__(self, filepath):

        self.filepath = filepath
        self.filename = self.filepath.split("/")[-1][:-7]
        # Import
        with open(self.filepath, "r") as f:
            data = [row.split() for row in f]
        for row in data:
            for element in range(len(row)):
                row[element] = float(row[element])
        for element in range(len(data[0])):
            data[0][element] = int(data[0][element])

        # Verteilungsart rausfinden, Abszissenwerte festlegen
        if data[0][0] > 1:
            self.direction = "X"
            pos = data[1]
        elif data[0][1] > 1:
            self.direction = "Y"
            pos = data[2]
        elif data[0][2] > 1:
            self.direction = "Z"
            pos = data[3]
            SSD = data[3][0] * 10

        self.unit = "mm"
        self.dose = data[4]
        self.std_dev = [data[4][i] * d for i, d in enumerate(data[5])]
        # pos-Werte = Voxelränder in mm, Umrechnen und mitteln
        pos_cm = [i * 10 for i in pos]
        pos_mittel = []
        for i in range(1, len(pos_cm)):
            pos_mittel.append(0.5 * (pos_cm[i] + pos_cm[i - 1]))
        # SSD abziehen falls TDK
        if self.direction == "Z":
            pos_mittel = [i - SSD for i in pos_mittel]

        self.axis = pos_mittel
        self.normpoint = max(self.dose)
        self.dose = {
            True: np.array(self.dose[len(self.dose) // 2 :]),
            False: np.array(self.dose),
        }
        self.axis = {True: self.axis[len(self.axis) // 2 :], False: self.axis}
        self.std_dev = {
            True: self.std_dev[len(self.std_dev) // 2 :],
            False: self.std_dev,
        }

    def params(self):
        if self.direction == "Z":
            return egspdd.calculate_parameters(
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
