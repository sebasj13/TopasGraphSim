# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 13:25:16 2021

@author: Sebastian Schäfer
@institution: Martin-Luther-Universität Halle-Wittenberg
@email: sebastian.schaefer@student.uni-halle.de
"""

import os
import re
import sys

import math
import numpy as np

import scipy.integrate as integrate
import scipy.interpolate as interpolate

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

from tkinter import simpledialog as sd


def load_exp_values():
    
    """
    A function to load experimental results as lists,
    which returns them in the proper format to be plotted.
    """
    
    xvals = np.array([])
    direction = "X"
    yvals = []
    maximum = max(yvals)
    yvals = np.array([value/maximum for value in yvals])
    std_dev = None
    
    return xvals, direction, yvals, std_dev

def read_data(path):
    
    """
    A function that reads the relevant data from a TOPAS simulation
    output file in ASCII format. Determines the type of data (depth
    dose or dose profile) and calculates the standard deviation.
    Uses the binning information to create the proper directional 
    scalingamd normalizes the maximum of the data to 1.
    """

    with open(path) as file:
        
        dose     = []
        std_dev  = []
        settings = []
        step_factor = 1
        hist = 0
        
        for line in file:
            
            if "# X" in line:
                x_settings = list(map(float,re.findall(r"[-+]?\d*\.\d+|\d+", line)))
                settings +=  [x_settings]
                if "cm" in line:
                    step_factor = 10
            if "# Y" in line:
                y_settings = list(map(float,re.findall(r"[-+]?\d*\.\d+|\d+", line)))
                settings += [y_settings]
                if "cm" in line:
                    step_factor = 10
            if "# Z" in line:
                z_settings = list(map(float,re.findall(r"[-+]?\d*\.\d+|\d+", line)))
                settings += [z_settings]
                if "cm" in line:
                    step_factor = 10
            
            if not "#" in line:
                
                values   = line.split(",")[3:]
                values   = [float(value.replace("e","E").replace("\n","")) for value in values]
                dose    += [values[0]]
                
                if hist == 0:
                    try:
                        histories = int(values[2])
                        hist = histories
                    except IndexError:
                        hist = sd.askinteger("Historien", "Anzahl der Historien in der Simulation:")
                        
                std_dev += [values[1] * math.sqrt(hist)] #* for sum, / for mean
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
        axis = [round(step/2 + i*step,3) for i in range(bins)]    
        
    else:
        if bins%2 == 0:
            pos_half = [round(step/2 + i*step,3) for i in range(int(bins/2))] 
            neg_half = pos_half[::-1]
            neg_half = [value*-1 for value in neg_half]   
            axis     = pos_half[::-1] + neg_half[::-1]   
        else:
            pos_half = [round(i*step,3) for i in range(int(bins/2)+1)]
            neg_half = [round(-i*step,3) for i in range(1,int(bins/2)+1)]
            axis     = pos_half[::-1] + neg_half 
    
    
    axis   = np.flip(np.array(axis))
    std_dev = np.array(std_dev)/max(dose) 
    dose    = np.array(dose)/max(dose)  
    
    return axis, direction, dose, std_dev


def calculate_pdd_parameters(axis, dose, std_dev):
    
    """
    A function to calculate the relevant 
    descriptive parameters of depth doses.
    """

    if type(std_dev) != np.ndarray:   
        TD20 = dose[(np.abs(axis-200)).argmin()] 
        TD10 = dose[(np.abs(axis-100)).argmin()]
        Q    = round(1.2661 * TD20/TD10 - 0.0595,5)
        zmax = round(axis[int(np.where(dose == 1)[0][0])],5)
        
        return [Q,0,zmax]

    new_step             = max([1/i for i in range(1,10) if int(axis[-1]*i) == round(float(axis[-1]*i),2)])
    interpolation_factor = int(round((axis[-2]-axis[-1])/new_step,0))
    interpolation_length = int(interpolation_factor * len(axis) - (interpolation_factor-1))
    
    interpolated_axis          = np.linspace(axis[0], axis[-1], interpolation_length)
    akima_stddev_interpolator   = interpolate.Akima1DInterpolator(np.flip(axis), std_dev)
    interpolated_stddev         = np.flip(akima_stddev_interpolator.__call__(interpolated_axis))
    akima_dose_interpolator     = interpolate.Akima1DInterpolator(np.flip(axis), dose)
    interpolated_dose           = np.flip(akima_dose_interpolator.__call__(interpolated_axis))
    
    interpolated_stddev = interpolated_stddev/max(interpolated_dose) 
    interpolated_dose   = interpolated_dose/max(interpolated_dose) 
    
    TD20  = interpolated_dose[int(np.where(interpolated_axis == 200)[0][0])]
    dTD20 = interpolated_stddev[int(np.where(interpolated_axis == 200)[0][0])]
    TD10  = interpolated_dose[int(np.where(interpolated_axis == 100)[0][0])]
    dTD10 = interpolated_stddev[int(np.where(interpolated_axis == 100)[0][0])]
    
    Q    = round(1.2661 * TD20/TD10 - 0.0595,5)
    dQ   = round(math.sqrt((1.2661*dTD20/TD10)**2 + (-1.2661*TD20*dTD10/TD10**2)**2),5)
    zmax = round(axis[int(np.where(dose == 1)[0][0])],5)
    
    return [Q, dQ, zmax]


def calculate_dp_parameters(axis, dose, std_dev):
    
    """
    A function to calculate the relevant
    descriptive parameters of dose profiles.
    """
    
    interpolated_axis           = np.linspace(axis[0], axis[-1], len(axis)*100)
    akima_dose_interpolator     = interpolate.Akima1DInterpolator(axis, dose)
    interpolated_dose           = np.flip(akima_dose_interpolator.__call__(interpolated_axis))
        
    Dose80 = [value for value in dose if value >= 0.8]
    
    D0   = (interpolated_dose[int(len(interpolated_dose)/2)]+interpolated_dose[int(len(interpolated_dose)/2)-1])/2
    XL20 = interpolated_axis[:int(len(interpolated_axis)/2)][(np.abs(interpolated_dose[:int(len(interpolated_axis)/2)]-0.2)).argmin()]
    XL50 = interpolated_axis[:int(len(interpolated_axis)/2)][(np.abs(interpolated_dose[:int(len(interpolated_axis)/2)]-0.5)).argmin()]
    XL80 = interpolated_axis[:int(len(interpolated_axis)/2)][(np.abs(interpolated_dose[:int(len(interpolated_axis)/2)]-0.8)).argmin()]
    XR20 = interpolated_axis[int(len(interpolated_axis)/2):][(np.abs(interpolated_dose[int(len(interpolated_axis)/2):len(interpolated_axis)]-0.2)).argmin()]
    XR50 = interpolated_axis[int(len(interpolated_axis)/2):][(np.abs(interpolated_dose[int(len(interpolated_axis)/2):len(interpolated_axis)]-0.5)).argmin()]
    XR80 = interpolated_axis[int(len(interpolated_axis)/2):][(np.abs(interpolated_dose[int(len(interpolated_axis)/2):len(interpolated_axis)]-0.8)).argmin()]

    
    HWB          = round(abs(XR50 - XL50),5)
    CAXdev       = round(XL50 + 0.5*HWB,5)

    flat_krieger = round(max([value for value in dose if value >= 0.95])-min([value for value in dose if value >= 0.95])/D0,5)
    flat_stddev  = round(np.std(Dose80),5)
    
    if len(Dose80)%2!=0:
        Dose80 = Dose80[0:int(len(Dose80)/2)] + Dose80[int(len(Dose80)/2)+1:len(Dose80)]
    
    S            = round(max([Dose80[i-1]/Dose80[len(Dose80)-i] for i in range(1,len(Dose80)+1)]),5)
    
    Lpenumbra    = round(abs(XL80-XL20),5)
    Rpenumbra    = round(abs(XR80-XR20),5)
    
    XL20index    = np.where(interpolated_axis == XL20)[0][0]
    XL80index    = np.where(interpolated_axis == XL80)[0][0]
    XR20index    = np.where(interpolated_axis == XR20)[0][0]
    XR80index    = np.where(interpolated_axis == XR80)[0][0]
    Lintegral    = round(abs(integrate.simps(interpolated_dose[XL20index:XL80index], interpolated_axis[XL20index:XL80index])),5)
    Rintegral    = round(abs(integrate.simps(interpolated_dose[XR80index:XR20index], interpolated_axis[XR80index:XR20index])),5)
    
    return  [HWB, CAXdev, flat_krieger, flat_stddev, S, Lpenumbra, Rpenumbra, Lintegral, Rintegral]


def create_plot(title, axis, direction, dose, std_dev, *args):
    
    """
    A function to create the depth dose or dose profile
    plot of the selected simulation result file. Includes
    the calculated descriptive parameters.
    """
    
    fig, ax = plt.subplots()
    plt.style.use("default")
    fig.set_dpi(600)
    fig.set_size_inches(10,5)
    
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(axis="both", which="minor", length = 2)
    
    xlabel = "{}-Achse [mm]".format(direction)
    ax.set_xlabel(xlabel, size=12)
    ax.set_ylabel("Relative Dosis", size=12)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.6)
    
    if len(args) == 3 :
        Q, dQ, zmax = args[0], args[1], args[2]
        textstr = "Q     = {} ± {}\n{} = {} mm".format(Q,dQ,"$z_{max}$",zmax)
        ax.text(0.75, 0.975, textstr, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=props)    
        
    else:
        HWB, CAXdev, flat_krieger, flat_stddev, S, Lpenumbra, Rpenumbra, Lintegral, Rintegral = args[0], args[1], args[2],\
            args[3], args[4], args[5], args[6], args[7], args[8]
        textstr = "HWB = {} mm\n{} = {} mm\n{} = {}\n{} = {}\n{} = {} mm\n{} = {} mm\n{} = {}\n{} = {}\n\
Symmetrie = {}".format(HWB, "$CAX_{dev}$", CAXdev, "$FLAT_{Krieger}$", flat_krieger, "$FLAT_{stddev}$", flat_stddev,\
"$Penumbra_{L}$", Lpenumbra, "$Penumbra_{R}$", Rpenumbra,"$Integral_{L}$", Lintegral, "$Integral_{R}$", Rintegral, S)   
        ax.text(0.5, 0.5, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props, horizontalalignment="center")
            
    ax.grid(True, which="major")
    ax.grid(True, which="minor", color="grey", linewidth=0.1)
    
    ax.errorbar(x = axis, y = dose, yerr = std_dev, fmt="go", \
                 ecolor="r",elinewidth=0.5, capsize=1, capthick=0.2, ms=2, label = "Simulation")
    ax.plot(axis, dose, "-.", color = "green", linewidth=0.5)

    plt.savefig("{}.png".format(title.replace(".csv","")), dpi=600, bbox_inches="tight")

    return 


def plot_args(path, exp=False):
    
    """
    A function that returns the correct plot parameters
    for the type of simulation performed.
    """
    
    if exp == True:
        axis, direction, dose, std_dev = load_exp_values()
    else:
        axis, direction, dose, std_dev = read_data(path)
              
    if direction == "Z":
        Q, dQ, zmax          = calculate_pdd_parameters(axis, dose, std_dev)

        return axis, direction, dose, std_dev, Q, dQ, zmax   
    
    else:
        HWB, CAXdev, flat_krieger, flat_stddev, S, Lpenumbra, Rpenumbra, Lintegral, Rintegral = calculate_dp_parameters(axis, dose, std_dev)

        return axis, direction, dose, std_dev, HWB, CAXdev, flat_krieger, flat_stddev, S, Lpenumbra, Rpenumbra, Lintegral, Rintegral

if __name__ == "__main__":
    
    try:
        path = sys.argv[1]
        histories = int(float(sys.argv[2]))
        if os.path.exists(path):
            create_plot(path,*plot_args(path, histories))
        else:
            print("\nInvalid input file!")
    except ValueError:
        print("\nInvalid history count!")
    except IndexError:
        print("\nNo input file! ")
