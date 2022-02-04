from scipy.interpolate import CubicSpline
import numpy as np


def calculate_parameters(axis, dose, std_dev):

    """
    A function to calculate the relevant 
    descriptive parameters of depth doses.
    """

    def findnearestdatapoint(listname, value):
        a = []
        for i in range(len(listname)):
            a.append(abs(listname[i] - value))
        return a.index(min(a))

    ################# Interpolate
    cs_sim = CubicSpline(axis, dose)
    posspline = np.arange(0, 300, 0.01)
    dosespline = cs_sim(posspline)
    # Berechnung Q

    ind20 = findnearestdatapoint(posspline, 200)
    ind10 = findnearestdatapoint(posspline, 100)
    TD20 = dosespline[ind20]
    TD10 = dosespline[ind10]
    Q = round(1.2661 * TD20 / TD10 - 0.0595, 5)  # DIN 6800-2
    dQ = 0
    # Berechnung zmax
    zmax = round(posspline[np.argmax(dosespline)], 5)

    return [Q, dQ, zmax]

