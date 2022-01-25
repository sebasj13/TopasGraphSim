import tkinter.simpledialog as sd

import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
from PIL import Image, ImageTk
from win32api import GetSystemMetrics

from ..resources.language import Text
from .measurement_import import Measurement
from .ptw_import import PTWMultimporter
from .sim_import import Simulation


class DoseFigureHandler:
    def __init__(self, parent, norm, zoom):

        self.parent = parent

        self.norm = norm
        self.zoom = zoom

        # Initialize the current settings
        self.lang = self.parent.lang
        self.text = Text()
        self.style = plt.style.use("default")
        self.current_mode = self.parent.dark.get()
        self.colors = {
            False: ["#ffa43c", "#ff2e1b", "#1bff67", "#ff5cf1", "#493cff"],
            True: ["#ff7fff", "#ffff00", "#00ffff", "#ff4040", "#40ff40"],
        }
        self.marker = "o--"
        self.markersize = self.parent.profile.get_attribute("markersize")
        self.linewidth = self.parent.profile.get_attribute("linewidth")
        # Initialize the figure and axes
        self.fig = Figure(figsize=(10, 5), constrained_layout=True, dpi=600)
        self.canvas = FigureCanvasAgg(self.fig)
        self.fig.set_canvas(self.canvas)
        self.ax = self.fig.add_subplot(111)

        # Initialize necessary variables
        self.props = dict(boxstyle="round", facecolor="wheat", alpha=0.6)
        self.plots = []
        self.data = []

    def set_style(self):

        """
        Switches the plotting style accordung to the current theme
        """

        if self.parent.dark.get() != self.current_mode:

            if self.parent.dark.get() == True:
                try:
                    self.ax.set_facecolor("#363636")
                    self.fig.set_facecolor("#363636")

                except AttributeError:
                    pass
            else:
                try:
                    self.ax.set_facecolor("#ffffff")
                    self.fig.set_facecolor("#ffffff")

                except AttributeError:
                    pass

            self.current_mode = self.parent.dark.get()

            if self.plots != []:
                self.parent.show_preview()

    def flush(self):

        """
        Clears the data
        """

        self.data = []

    def fits(self, image):

        """
        Scales an image to the width of the screen.
        """

        scr_width = GetSystemMetrics(0)
        width = int(scr_width)
        scale_factor = image.shape[1] / width
        image = cv2.resize(
            image,
            (width, int(image.shape[0] / scale_factor)),
            interpolation=cv2.INTER_AREA,
        )

        return image

    def set_axis(self):

        """
        Defines the layout and gridlines of the plot 
        """

        self.ax.clear()
        self.ax.grid(True, which="major")
        self.ax.grid(True, which="minor", color="grey", linewidth=0.1)
        self.ax.xaxis.set_minor_locator(AutoMinorLocator())
        self.ax.yaxis.set_minor_locator(AutoMinorLocator())
        self.ax.tick_params(axis="both", which="minor", length=2)

    def add_plot_data(self, datanames):

        """
        Adds data to the plot queue
        """

        test = [plotdata.direction for plotdata in self.plots]
        for tuple in datanames:
            filename = tuple[0]
            type = tuple[1]
            if filename not in [plotdata.filepath for plotdata in self.plots]:
                if type == "simulation":
                    sim = Simulation(filename)
                    if test == []:
                        self.plots += [sim]
                    elif sim.direction in test:
                        self.plots += [sim]
                    else:
                        sd.messagebox.showinfo(
                            "", f"{sim.filename}" + self.text.incordata[self.lang][1]
                        )
                elif type == "ptw":
                    importer = PTWMultimporter(filename, self.parent.parent)
                    importer.window.mainloop()
                    measurements = [plot for plot in importer.plots]
                    fails = []
                    for plot in measurements:
                        if test == []:
                            self.plots += [plot]
                        elif plot.direction in test:
                            self.plots += [plot]
                        else:
                            fails += [plot]

                    if fails != []:
                        names = ""
                        for f in fails:
                            names += str(f.filename) + ", "
                        names = names[:-2]
                        var = 1
                        if len(fails) >= 2:
                            var = 2
                        sd.messagebox.showinfo(
                            "", f"{names}" + self.text.incordata[self.lang][var],
                        )

                    importer.window.destroy()
                    del importer

                else:
                    self.plots += [Measurement(filename, type)]

        for plotdata in self.plots:
            if self.norm == True:
                self.data += [
                    [
                        plotdata.axis,
                        plotdata.direction,
                        plotdata.norm_dose,
                        plotdata.norm_std_dev,
                    ]
                    + plotdata.params
                ]
            else:
                self.data += [
                    [
                        plotdata.axis,
                        plotdata.direction,
                        plotdata.dose,
                        plotdata.std_dev,
                    ]
                    + plotdata.params
                ]

    def add_legend(self):

        """
        Adds the legend
        """

        self.ax.legend(
            loc="upper right",
            framealpha=0.6,
            facecolor="wheat",
            edgecolor="black",
            fancybox=True,
        )

    def add_descriptors(self):

        """
        Adds the calculated parameters as descriptors
        """

        for index, plot_data in enumerate(self.data):

            if len(plot_data) == 7:
                Q, dQ, zmax = plot_data[4], plot_data[5], plot_data[6]
                textstr = "Q     = {} ± {}\n{} = {} mm".format(Q, dQ, "$z_{max}$", zmax)
                space = 0
                if dQ == 0:
                    space = 0.05
                if len(str(Q)) == 6:
                    space += 0.01
                if len(str(dQ)) == 6:
                    space += 0.01
                self.ax.text(
                    0.795 + space,
                    0.7 - 0.1 * index,
                    textstr,
                    transform=self.ax.transAxes,
                    fontsize=10,
                    verticalalignment="top",
                    bbox=self.props,
                    color=self.colors[self.current_mode][index],
                )
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
                ) = (
                    plot_data[4],
                    plot_data[5],
                    plot_data[6],
                    plot_data[7],
                    plot_data[8],
                    plot_data[9],
                    plot_data[10],
                    plot_data[11],
                    plot_data[12],
                )
                textstr = "{} = {} mm\n{} = {} mm\n{} = {}\n{} = {}\n{} = {} mm\n{} = {} mm\n{} = {}\n{} = {}\n{} = {}".format(
                    self.text.fwhm[self.lang],
                    HWB,
                    "$CAX_{dev}$",
                    CAXdev,
                    "$FLAT_{Krieger}$",
                    flat_krieger,
                    "$FLAT_{stddev}$",
                    flat_stddev,
                    "$Penumbra_{L}$",
                    Lpenumbra,
                    "$Penumbra_{R}$",
                    Rpenumbra,
                    "$Integral_{L}$",
                    Lintegral,
                    "$Integral_{R}$",
                    Rintegral,
                    self.text.symmetry[self.lang],
                    S,
                )

                self.ax.text(
                    (0.6 - 0.1 * len(self.data)) + 0.2 * index,
                    0.5,
                    textstr,
                    transform=self.ax.transAxes,
                    fontsize=10,
                    verticalalignment="top",
                    bbox=self.props,
                    horizontalalignment="center",
                    color=self.colors[self.current_mode][index],
                )

    def set_x_label(self):

        """
        Names the x-axis according to the plot
        """
        xlabel = "{}-{} [mm]".format(self.data[0][1], self.text.axis[self.lang])
        self.ax.set_xlabel(xlabel, size=12)
        if self.norm == False:
            self.ax.set_ylabel(self.plots[0].unit, size=12)

    def create_plots_from_data(self):

        """
        Creates the plots from the queue
        """

        for index, plot_data in enumerate(self.data):
            self.ax.errorbar(
                x=plot_data[0],
                y=plot_data[2],
                yerr=plot_data[3],
                fmt="none",
                ecolor="black",
                elinewidth=0.5,
                capsize=1,
                capthick=0.2,
                ms=2,
            )
            self.ax.plot(
                plot_data[0],
                plot_data[2],
                self.marker,
                markersize=self.markersize,
                color=self.colors[self.current_mode][index],
                linewidth=self.linewidth,
                label=f"{self.plots[index].filename}",
            )

        try:
            self.axins.remove()
        except:
            pass

        if self.zoom == True:

            self.canvas.draw()
            self.transform = self.ax.transData
            self.inverted_transform = self.ax.transData.inverted()
            width, height = self.fig.canvas.get_width_height()

            self.focuspoint = self.plots[-1].axis[len(self.plots[-1].axis) // 2]
            try:
                self.focuspoint = self.inverted_transform.transform(
                    (
                        width
                        * (self.parent.canvas.coords(self.parent.oval)[0] + 5)
                        / self.parent.canvas.image.width(),
                        1,
                    )
                )
                self.focuspoint = self.plots[-1].axis[
                    np.abs(
                        np.asarray(self.plots[-1].axis - self.focuspoint[0])
                    ).argmin()
                ]
            except AttributeError:
                pass
            except IndexError:
                pass

            pixels = self.transform.transform(np.vstack([plot_data[0], plot_data[2]]).T)
            x, y = pixels.T
            y = height - y

            self.pixelx = x[self.plots[-1].axis.index(self.focuspoint)] / width
            self.pixely = y[self.plots[-1].axis.index(self.focuspoint)] / height

            self.axins = inset_axes(self.ax, "28%", "28%", loc="lower left")
            yvalsat195 = []
            yvalsat205 = []
            for index, plot_data in enumerate(self.data):
                self.axins.errorbar(
                    x=plot_data[0],
                    y=plot_data[2],
                    yerr=plot_data[3],
                    fmt="none",
                    ecolor="black",
                    elinewidth=0.5,
                    capsize=1,
                    capthick=0.2,
                    ms=2,
                )
                self.axins.plot(
                    plot_data[0],
                    plot_data[2],
                    self.marker,
                    markersize=self.markersize,
                    color=self.colors[self.current_mode][index],
                    linewidth=self.linewidth,
                    label=f"{self.plots[index].filename}",
                )
                yvalsat195 += [
                    plot_data[2][
                        plot_data[0].index(
                            min(
                                plot_data[0],
                                key=lambda x: abs(x - (self.focuspoint - 5)),
                            )
                        )
                    ]
                ]
                yvalsat205 += [
                    plot_data[2][
                        plot_data[0].index(
                            min(
                                plot_data[0],
                                key=lambda x: abs(x - (self.focuspoint + 5)),
                            )
                        )
                    ]
                ]

            # sub region of the original image
            x1, x2, y1, y2 = (
                self.focuspoint - 6,
                self.focuspoint + 6,
                0.99 * min(yvalsat205),
                1.01 * max(yvalsat195),
            )
            self.axins.set_xlim(x1, x2)
            self.axins.set_ylim(y1, y2)
            self.axins.tick_params(
                labelleft=False, labelbottom=False, bottom=False, left=False
            )

            mark_inset(self.ax, self.axins, loc1=2, loc2=4, fc="none", ec="0.5")

    def return_figure(self, filenames):

        """
        Passes the image of the plot and the plot type to the MainApplication
        """

        self.set_axis()
        self.add_plot_data(filenames)
        self.set_style()
        self.set_x_label()
        self.create_plots_from_data()
        self.add_legend()
        self.add_descriptors()

        self.canvas.draw()
        buffer = self.canvas.buffer_rgba()
        image_array = np.asarray(buffer)
        fit_array = self.fits(image_array)
        image = Image.fromarray(fit_array)
        photoimage = ImageTk.PhotoImage(image)

        return photoimage, self.data[0][1]
