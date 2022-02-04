import math

import numpy as np
import scipy.interpolate as interpolate


def calculate_parameters(axis, dose, std_dev):

    """
    A function to calculate the relevant 
    descriptive parameters of depth doses.
    """

    axis = np.flip(axis).tolist()
    dose = np.flip(dose)
    std_dev = np.flip(std_dev)

    if type(std_dev) != np.ndarray or std_dev == []:
        TD20 = dose[(np.abs(axis - 200)).argmin()]
        TD10 = dose[(np.abs(axis - 100)).argmin()]
        Q = round(1.2661 * TD20 / TD10 - 0.0595, 5)
        zmax = round(axis[int(np.where(dose == max(dose))[0][0])], 5)

        return [Q, 0, zmax]

    new_step = max(
        [
            1 / i
            for i in range(1, 10)
            if int(axis[-1] * i) == round(float(axis[-1] * i), 2)
        ]
    )
    interpolation_factor = int(round((axis[-2] - axis[-1]) / new_step, 0))
    interpolation_length = int(
        interpolation_factor * len(axis) - (interpolation_factor - 1)
    )

    interpolated_axis = np.linspace(axis[0], axis[-1], interpolation_length)
    akima_stddev_interpolator = interpolate.Akima1DInterpolator(np.flip(axis), std_dev)
    interpolated_stddev = np.flip(akima_stddev_interpolator.__call__(interpolated_axis))
    akima_dose_interpolator = interpolate.Akima1DInterpolator(np.flip(axis), dose)
    interpolated_dose = np.flip(akima_dose_interpolator.__call__(interpolated_axis))

    interpolated_stddev = interpolated_stddev / max(interpolated_dose)
    interpolated_dose = interpolated_dose / max(interpolated_dose)

    TD20 = interpolated_dose[int(np.where(interpolated_axis == 200)[0][0])]
    dTD20 = interpolated_stddev[int(np.where(interpolated_axis == 200)[0][0])]
    TD10 = interpolated_dose[int(np.where(interpolated_axis == 100)[0][0])]
    dTD10 = interpolated_stddev[int(np.where(interpolated_axis == 100)[0][0])]

    Q = round(1.2661 * TD20 / TD10 - 0.0595, 5)
    dQ = round(
        math.sqrt(
            (1.2661 * dTD20 / TD10) ** 2 + (-1.2661 * TD20 * dTD10 / TD10 ** 2) ** 2
        ),
        5,
    )
    zmax = round(axis[int(np.where(dose == max(dose))[0][0])], 5)

    return [Q, dQ, zmax]
