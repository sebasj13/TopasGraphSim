# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 12:47:50 2021

@author: Sebastian Schäfer
@institution: Martin-Luther-Universität Halle-Wittenberg
@email: sebastian.schaefer@student.uni-halle.de
"""

import os
import numpy as np

import cv2
from PIL import Image, ImageTk

from create_pdd_or_dp_plot import *

from win32api import GetSystemMetrics

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
from tkinter import simpledialog as sd

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator
from matplotlib.backends.backend_agg import FigureCanvasAgg


def fig_to_arr(title, axis, direction, dose, std_dev, *args):
    
    """
    A function that creates a dope profile or
    depth dose plot and returns it as an array.
    """
    
    fig = Figure(figsize=(10,5), dpi=1200)
    canvas = FigureCanvasAgg(fig)
    ax = fig.add_subplot(111)
    
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
        HWB, CAXdev, flat_krieger, flat_stddev, S, Lpenumbra, Rpenumbra, Lintegral, Rintegral = \
        args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8]
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
        
    canvas.draw()
    buf = canvas.buffer_rgba()
    arr = np.asarray(buf)
    
    return arr        

def fits(image):
    
    """
    A function that scales an image to the width of the screen.
    """
    
    scr_width = GetSystemMetrics(0)
    width = int(scr_width)   
    scale_factor = image.shape[1]/width
    image = cv2.resize(image, (width, int(image.shape[0]/scale_factor)),\
                       interpolation = cv2.INTER_AREA)
            
    return image

class MainApplication(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
             
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack(side="top", fill="both", expand=True)
        
        self.menubar = tk.Menu(self.parent)
        self.filemenu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="Datei", menu=self.filemenu)
        
        self.filemenu.add_command(label="Simulationsergebnis laden", command = self.load_file) 
        self.filemenu.add_command(label="Ergebnis abspeichern", command = self.save_graph)
        self.filemenu.entryconfig(1,state=tk.DISABLED)
        self.filemenu.add_command(label="Derzeitige Simulation schließen", command = self.close_file)
        self.filemenu.entryconfig(2,state=tk.DISABLED)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Beenden", command = self.parent.destroy)
        self.parent.config(menu=self.menubar)
         
        self.canvas = None
        self.filename = None
        self.histories = None
        self.graph = None

    def load_file(self):
        
        self.filetypes = [("Simulationsergebnisse", ".csv")]
        self.filename = fd.askopenfilename(title='Datei auswählen...',initialdir=os.getcwd(),filetypes=self.filetypes)
        if self.filename == "":
            return
        self.show_preview()
        self.filemenu.entryconfig(0,state=tk.DISABLED)
        self.filemenu.entryconfig(1,state=tk.NORMAL)
        self.filemenu.entryconfig(2,state=tk.NORMAL)
        
    def close_file(self):
        
        self.canvas.pack_forget()
        self.filemenu.entryconfig(0,state=tk.NORMAL)
        self.filemenu.entryconfig(1,state=tk.DISABLED)
        self.filemenu.entryconfig(2,state=tk.DISABLED)
        
    def save_graph(self):
        
        self.graph.save(self.filename.replace(".csv",".png"))
        
    def show_preview(self):
        
        self.array = fig_to_arr(self.filename, *plot_args(self.filename))
        self.fit_array = fits(self.array)
        self.image = Image.fromarray(self.fit_array)
        self.graph = Image.fromarray(self.array)
        self.photoimage = ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0,0, anchor=tk.NW, image=self.photoimage)
        self.canvas.image = self.photoimage

   
root = tk.Tk()
root.geometry("960x540")
root.state('zoomed')
root.title("Simulationsauswertung")
style = ttk.Style(root)
root.tk.call('source', str(os.getcwd())+'\\Azure-ttk-theme\\azure.tcl')
root.tk.call("set_theme", "dark")
Main = MainApplication(root)
root.mainloop()
