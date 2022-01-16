# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 13:25:16 2021

@author: Sebastian Schäfer
@institution: Martin-Luther-Universität Halle-Wittenberg
@email: sebastian.schaefer@student.uni-halle.de
"""

from main.functions import dp, pdd, read_measurement, read_simulation


def plot_args(path, type):

    """
    A function that returns the correct plot parameters
    for the type of simulation performed.
    """

    if type == "simulation":
        axis, direction, dose, std_dev = read_simulation.load(path)
    else:
        axis, direction, dose, std_dev = read_measurement.load(path, type)

    if direction == "Z":
        Q, dQ, zmax = pdd.calculate_parameters(axis, dose, std_dev)

        return axis, direction, dose, std_dev, Q, dQ, zmax

    else:
        (
            HWB,
            CAXdev,
            flat_krieger,
            flat_stddev,
            S,
            Lpenumbra,
            Rpenumbra,
            Lintegral,
            Rintegral,
        ) = dp.calculate_parameters(axis, dose, std_dev)

        return (
            axis,
            direction,
            dose,
            std_dev,
            HWB,
            CAXdev,
            flat_krieger,
            flat_stddev,
            S,
            Lpenumbra,
            Rpenumbra,
            Lintegral,
            Rintegral,
        )

