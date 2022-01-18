import math
import re
from tkinter import simpledialog as sd

import numpy as np


def load(path):

    """
    A function that reads the relevant data from a TOPAS simulation
    output file in ASCII format. Determines the type of data (depth
    dose or dose profile) and calculates the standard deviation.
    Uses the binning information to create the proper directional 
    scaling and normalizes the maximum of the data to 1.
    """

    with open(path) as file:

        dose = []
        std_dev = []
        settings = []
        step_factor = 1
        hist = 0

        for line in file:

            if "# R" in line or "# Phi" in line:
                x_settings = []
                y_settings = []

            if "# X" in line:
                x_settings = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", line)))
                settings += [x_settings]
                if "cm" in line:
                    step_factor = 10
            if "# Y" in line:
                y_settings = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", line)))
                settings += [y_settings]
                if "cm" in line:
                    step_factor = 10
            if "# Z" in line:
                z_settings = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", line)))
                settings += [z_settings]
                if "cm" in line:
                    step_factor = 10

            if not "#" in line:

                values = line.split(",")[3:]
                values = [
                    float(value.replace("e", "E").replace("\n", "")) for value in values
                ]
                dose += [values[0]]

                if hist == 0:
                    try:
                        histories = int(values[2])
                        hist = histories
                    except IndexError:
                        hist = sd.askinteger(
                            "Historien", "Anzahl der Historien in der Simulation:"
                        )

                std_dev += [values[1] * math.sqrt(hist)]  # * for sum, / for mean
        if max(max(settings)) in x_settings:
            direction = "X"
            bins = int(x_settings[0])
            step = x_settings[1]

        elif max(max(settings)) in y_settings:
            direction = "Y"
            bins = int(y_settings[0])
            step = y_settings[1]

        else:
            direction = "Z"
            bins = int(z_settings[0])
            step = z_settings[1]

        step = step * step_factor

    if direction == "Z":
        axis = [round(step / 2 + i * step, 3) for i in range(bins)]

    else:
        if bins % 2 == 0:
            pos_half = [round(step / 2 + i * step, 3) for i in range(int(bins / 2))]
            neg_half = pos_half[::-1]
            neg_half = [value * -1 for value in neg_half]
            axis = pos_half[::-1] + neg_half[::-1]
        else:
            pos_half = [round(i * step, 3) for i in range(int(bins / 2) + 1)]
            neg_half = [round(-i * step, 3) for i in range(1, int(bins / 2) + 1)]
            axis = pos_half[::-1] + neg_half

    axis = np.flip(np.array(axis))
    std_dev = np.array(std_dev) / max(dose)
    dose = np.array(dose) / max(dose)

    return axis, direction, dose, std_dev
