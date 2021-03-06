import tkinter.messagebox as mb
import tkinter.simpledialog as sd

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pymedphys
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
from PIL import Image, ImageTk

from ..functions import dp
from ..resources.language import Text
from .egs_import import EGSSimulation
from .measurement_import import Measurement
from .ptw_import import PTWMultimporter
from .radcalc_import import RadCalc
from .sim_import import Simulation


class DoseFigureHandler:
    def __init__(self, parent):

        self.parent = parent

        self.norm = self.parent.norm.get()
        self.calcparams = self.parent.calcparams.get()
        self.normvalue = "max"
        self.errlimval = "absolute"
        self.errlimmin = 1.1
        self.errlimmax = 1.1
        self.errorbars = True
        self.caxcorrection = False
        self.title = None
        self.xaxisname = None
        self.yaxisname = None
        self.diffplot = False
        self.zoom = self.parent.zoom.get()
        self.half = self.parent.half.get()
        self.axlims = (self.parent.axlims.get(), self.parent.axlims.get())
        self.addmenu = False

        # Initialize the current settings
        self.lang = self.parent.lang
        self.text = Text()
        self.style = plt.style.use("default")
        self.colors = self.parent.profile.get_attribute("colors")
        self.marker = self.parent.profile.get_attribute("markers")
        self.markersize = self.parent.profile.get_attribute("markersize")
        self.linewidth = self.parent.profile.get_attribute("linewidth")

        # Initialize necessary variables
        self.props = dict(boxstyle="round", facecolor="wheat", alpha=0.6)
        self.plots = []

        self.difference = []

    def add_plot_data(self, datanames):

        """Adds data to the plot queue
        """
        self.data = []
        test = self.parent.direction
        for tuple in datanames:
            filename = tuple[0]
            type = tuple[1]
            if filename not in [plotdata.filepath for plotdata in self.plots]:
                if type == "simulation" or type == "egs":

                    if type == "simulation":
                        sim = Simulation(filename)
                    elif type == "egs":
                        sim = EGSSimulation(filename)

                    if test == None:
                        self.plots += [sim]
                        self.parent.direction = sim.direction
                        test = self.parent.direction
                    elif test == "Z" and sim.direction == "Z":
                        self.plots += [sim]
                    elif test == "X" and sim.direction == "X":
                        self.plots += [sim]
                    elif test == "Y" and sim.direction == "X":
                        self.plots += [sim]
                    elif test == "X" and sim.direction == "Y":
                        self.plots += [sim]
                    elif test == "Y" and sim.direction == "Y":
                        self.plots += [sim]
                    else:
                        sd.messagebox.showinfo(
                            "", f"{sim.filename}" + self.text.incordata[self.lang][1]
                        )
                        self.parent.filenames.pop(-1)

                elif type == "ptw":
                    importer = PTWMultimporter(filename, self.parent)
                    importer.window.mainloop()
                    importer.window.destroy()
                    measurements = [plot for plot in importer.plots]
                    fails = []
                    for plot in measurements:
                        if test == None:
                            self.plots += [plot]
                            self.parent.direction = plot.direction
                            test = self.parent.direction
                        elif test == "Z" and plot.direction == "Z":
                            self.plots += [plot]
                        elif test == "X" and plot.direction == "X":
                            self.plots += [plot]
                        elif test == "Y" and plot.direction == "X":
                            self.plots += [plot]
                        elif test == "X" and plot.direction == "Y":
                            self.plots += [plot]
                        elif test == "Y" and plot.direction == "Y":
                            self.plots += [plot]
                        else:
                            fails += [plot]

                    if fails != []:
                        self.parent.filenames.pop(-1)
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

                    del importer

                elif type == "measurement":
                    measurement = Measurement(filename, self.parent)
                    if test == None:
                        self.plots += [measurement]
                        self.parent.direction = measurement.direction
                        test = self.parent.direction
                    elif test == "Z" and measurement.direction == "Z":
                        self.plots += [measurement]
                    elif test == "X" and measurement.direction == "X":
                        self.plots += [measurement]
                    elif test == "Y" and measurement.direction == "X":
                        self.plots += [measurement]
                    elif test == "X" and measurement.direction == "Y":
                        self.plots += [measurement]
                    elif test == "Y" and measurement.direction == "Y":
                        self.plots += [measurement]
                    else:
                        sd.messagebox.showinfo(
                            "",
                            f"{measurement.filename}"
                            + self.text.incordata[self.lang][1],
                        )
                        self.parent.filenames.pop(-1)

                elif type == "radcalc":
                    radcalc = RadCalc(filename, self.parent)
                    if test == None:
                        self.plots += [radcalc]
                        self.parent.direction = radcalc.direction
                        test = self.parent.direction
                    elif test == "Z" and radcalc.direction == "Z":
                        self.plots += [radcalc]
                    elif test == "X" and radcalc.direction == "X":
                        self.plots += [radcalc]
                    elif test == "Y" and radcalc.direction == "X":
                        self.plots += [radcalc]
                    elif test == "X" and radcalc.direction == "Y":
                        self.plots += [radcalc]
                    elif test == "Y" and radcalc.direction == "Y":
                        self.plots += [radcalc]
                    else:
                        sd.messagebox.showinfo(
                            "",
                            f"{radcalc.filename}" + self.text.incordata[self.lang][1],
                        )
                        self.parent.filenames.pop(-1)

        if self.plots[0].direction == "Z":
            self.half = False

        for plotdata in self.plots:
            if self.norm == True:
                if self.normvalue == "max":
                    plotdata.normpoint = max(plotdata.dose[self.half])
                elif self.normvalue == "plateau":
                    plotdata.normpoint = np.average(
                        [
                            plotdata.dose[self.half][
                                len(plotdata.dose[self.half]) // 2
                                - 5 : len(plotdata.dose[self.half]) // 2
                                + 5
                            ]
                        ]
                    )

                else:
                    plotdata.normpoint = plotdata.dose[self.half][
                        len(plotdata.dose) // 2
                    ]

            else:
                plotdata.normpoint = 1

            caxdev = 0
            if self.caxcorrection == True:
                caxdev = dp.calculate_parameters(
                    plotdata.axis[False], plotdata.dose[False], True
                )

            self.data += [
                [
                    np.array([x + caxdev for x in plotdata.axis[self.half]]).tolist(),
                    plotdata.direction,
                    plotdata.dose[self.half] / plotdata.normpoint,
                    np.array(
                        [x / plotdata.normpoint for x in plotdata.std_dev[self.half]]
                    ),
                ]
            ]

        return

    def difference_plot(self):

        if self.plots[0].direction == "Z":
            self.figsize = [10, 5]
        else:
            self.figsize = [10, 6]

        if self.diffplot == True:

            self.figsize[1] *= 1.33333

            gs_kw = dict(height_ratios=[3, 1])
            self.fig, axd = plt.subplot_mosaic(
                [["top"], ["bottom"]],
                gridspec_kw=gs_kw,
                figsize=self.figsize,
                constrained_layout=True,
                sharex=True,
                dpi=600,
            )
            self.ax = axd["top"]
            self.diffax = axd["bottom"]

        else:
            self.fig = Figure(self.figsize, constrained_layout=True, dpi=600)
            self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasAgg(self.fig)
        self.fig.set_canvas(self.canvas)
        self.set_style()

        if self.diffplot == True:

            data = []
            for index, plot_data in enumerate(self.data[:2]):

                data += [[plot_data[0], plot_data[2]]]

            if np.all(np.diff(data[1][0]) > 0) == False:
                interpolated_data = np.flip(
                    np.interp(
                        np.flip(data[0][0]), np.flip(data[1][0]), np.flip(data[1][1])
                    )
                )
            else:
                interpolated_data = np.interp(
                    data[0][0], data[1][0], data[1][1], left=0, right=0
                )

            if self.errlimval == "absolute":
                self.difference = [
                    (interpolated_data[i] - data[0][1][i])  # / (data[0][1][i])
                    for i in range(len(data[0][0]))
                ]
            else:
                self.difference = [
                    100 * (interpolated_data[i] - data[0][1][i]) / (data[0][1][i])
                    for i in range(len(data[0][0]))
                ]

                self.difference[:] = [
                    x if round(x, 1) != -100 else 0 for x in self.difference
                ]
                self.difference[:] = [
                    x if round(x, 1) != 100 else 0 for x in self.difference
                ]

            label = self.text.error[self.lang] + " [abs]"
            if self.errlimval != "absolute":
                label = label[:-6] + " [%]"

            self.diffax.plot(
                data[0][0],
                self.difference,
                color=self.textcolor,
                linewidth=0.6,
                label=label,
            )

            self.errlim = [
                min(self.difference) * self.errlimmin,
                max(self.difference) * self.errlimmax,
            ]
            self.diffax.set_ylim(self.errlim)
            self.diffax.legend(
                loc="upper right",
                framealpha=0.6,
                facecolor="wheat",
                edgecolor="black",
                fancybox=True,
            )
        return

    def set_style(self):

        """Switches the plotting style according to the current theme
        """

        if self.parent.dark.get() == True:
            self.textcolor = "white"
            self.ax.set_facecolor("#363636")
            self.fig.set_facecolor("#363636")
            if self.diffplot == True:
                self.diffax.set_facecolor("#363636")
        else:
            self.textcolor = "black"
            self.ax.set_facecolor("#ffffff")
            self.fig.set_facecolor("#ffffff")
            if self.diffplot == True:
                self.diffax.set_facecolor("#ffffff")

        self.ax.xaxis.label.set_color(self.textcolor)
        self.ax.yaxis.label.set_color(self.textcolor)

        self.ax.tick_params(axis="x", colors=self.textcolor)
        self.ax.tick_params(axis="y", colors=self.textcolor)

        self.ax.spines["left"].set_color(self.textcolor)
        self.ax.spines["bottom"].set_color(self.textcolor)

        plt.rcParams.update(
            {"text.color": self.textcolor, "axes.labelcolor": self.textcolor}
        )

        if self.diffplot == True:
            self.diffax.xaxis.label.set_color(self.textcolor)
            self.diffax.yaxis.label.set_color(self.textcolor)

            self.diffax.tick_params(axis="x", colors=self.textcolor)
            self.diffax.tick_params(axis="y", colors=self.textcolor)

            self.diffax.spines["left"].set_color(self.textcolor)
            self.diffax.spines["bottom"].set_color(self.textcolor)

        return

    def flush(self):

        """Clears the data
        """

        self.data = []

        return

    def fits(self, image):

        """Scales an image to the width of the screen.
        """

        width = self.parent.parent.winfo_screenwidth()
        scale_factor = image.shape[1] / width
        image = cv2.resize(
            image,
            (width, int(image.shape[0] / scale_factor)),
            interpolation=cv2.INTER_AREA,
        )

        return image

    def set_axis(self):

        """Defines the layout and gridlines of the plot 
        """

        self.ax.clear()
        self.ax.grid(True, which="major")
        self.ax.grid(True, which="minor", color="grey", linewidth=0.1)
        self.ax.xaxis.set_minor_locator(AutoMinorLocator())
        self.ax.yaxis.set_minor_locator(AutoMinorLocator())
        self.ax.tick_params(axis="both", which="minor", length=2)

        if self.diffplot == True:
            self.diffax.grid(True, which="major")
            self.diffax.grid(True, which="minor", color="grey", linewidth=0.1)
            self.diffax.xaxis.set_minor_locator(AutoMinorLocator())
            self.diffax.yaxis.set_minor_locator(AutoMinorLocator())
            self.diffax.tick_params(axis="both", which="minor", length=2)

        return

    def add_legend(self):

        """Adds the legend
        """

        self.ax.legend(
            loc="upper right",
            framealpha=0.6,
            facecolor="wheat",
            edgecolor="black",
            fancybox=True,
        )

        return

    def add_descriptors(self):

        """Adds the calculated parameters as descriptors
        """

        temp = self.data
        new_data = []
        for index, data in enumerate(self.data):
            params = self.plots[index].params()
            new_data += [[data, params]]

        self.data = new_data
        if self.plots[0].direction != "Z":

            if self.half == False:
                positionsx = [
                    0.1,
                    0.1,
                    0.901,
                    0.901,
                    0.1,
                ]
                positionsy = [0.98, 0.68, 0.75, 0.45, 0.38]
            else:
                positionsx = [
                    0.7,
                    0.7,
                    0.901,
                    0.901,
                    0.7,
                ]
                positionsy = [0.98, 0.68, 0.68, 0.38, 0.38]

        for index, plot_data in enumerate(self.data):

            if len(plot_data[1]) == 3:

                Q, dQ, zmax = plot_data[1][0], plot_data[1][1], plot_data[1][2]
                textstr = "Q     = {} ?? {}\n{} = {} mm".format(Q, dQ, "$z_{max}$", zmax)
                space = 0
                if dQ == 0:
                    space = 0.05
                if len(str(Q)) == 6:
                    space += 0.01
                if len(str(dQ)) == 6:
                    space += 0.01
                self.ax.text(
                    0.795 + space,
                    0.955 - len(self.plots) * 0.0475 - 0.1 * index,
                    textstr,
                    transform=self.ax.transAxes,
                    fontsize=10,
                    verticalalignment="top",
                    bbox=self.props,
                    color=self.colors[index],
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
                    plot_data[1][0],
                    plot_data[1][1],
                    plot_data[1][2],
                    plot_data[1][3],
                    plot_data[1][4],
                    plot_data[1][5],
                    plot_data[1][6],
                    plot_data[1][7],
                    plot_data[1][8],
                )

                if self.caxcorrection == True:
                    CAXdev = 0

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
                    positionsx[index],
                    positionsy[index],
                    textstr,
                    transform=self.ax.transAxes,
                    fontsize=10,
                    verticalalignment="top",
                    bbox=self.props,
                    horizontalalignment="center",
                    color=self.colors[index],
                )
        self.data = temp
        return

    def set_x_label(self):

        """Names the x-axis according to the plot type
        """

        directions = [plot.direction for plot in self.plots]
        if directions.count(directions[0]) == len(directions):

            self.xlabel = f"{directions[0]}-{self.text.axis[self.lang]} [mm]"
        else:
            self.xlabel = (
                f"X- {self.text.orr[self.lang]} Y-{self.text.axis[self.lang]} [mm]"
            )

        if self.diffplot == True:
            if self.xaxisname != None:
                self.diffax.set_xlabel(self.xaxisname, size=12)
            else:
                self.diffax.set_xlabel(self.xlabel, size=12)
        else:
            if self.xaxisname != None:
                self.ax.set_xlabel(self.xaxisname, size=12)
            else:
                self.ax.set_xlabel(self.xlabel, size=12)

        if self.yaxisname == None:
            self.ax.set_ylabel(self.text.normunit[self.lang], size=12)
            if self.norm == False:
                self.ax.set_ylabel(self.plots[0].unit, size=12)
        else:
            self.ax.set_ylabel(self.yaxisname, size=12)

        return

    def create_plots_from_data(self):

        """Creates the plots from the queue
        """

        for index, plot_data in enumerate(self.data):

            if self.errorbars == True:
                try:
                    self.ax.errorbar(
                        x=plot_data[0],
                        y=plot_data[2],
                        yerr=plot_data[3],
                        fmt="none",
                        ecolor=self.colors[index],
                        elinewidth=0.625,
                        capsize=1.25,
                        capthick=0.25,
                        ms=2.5,
                    )
                except ValueError:
                    pass
            self.ax.plot(
                plot_data[0],
                plot_data[2],
                self.marker[index],
                markersize=self.markersize,
                color=self.colors[index],
                linewidth=self.linewidth,
                label=f"{self.plots[index].filename}",
            )

        try:
            self.axins.remove()
        except:
            pass

        self.set_xlims()

        if self.zoom == True:

            self.canvas.draw()
            self.transform = self.ax.transData
            self.inverted_transform = self.ax.transData.inverted()
            width, height = self.fig.canvas.get_width_height()

            extent = max([max(plot.axis[self.half]) for plot in self.plots])
            reference = [
                plot for plot in self.plots if max(plot.axis[self.half]) == extent
            ][-1]

            try:
                self.focuspoint = self.inverted_transform.transform(
                    (
                        width
                        * (
                            -(
                                self.parent.canvas.winfo_width()
                                - self.parent.canvas.image.width()
                            )
                            // 2
                            + self.parent.canvas.coords(self.parent.oval)[0]
                            + 5
                        )
                        / self.parent.canvas.image.width(),
                        abs(
                            height
                            * (
                                -(
                                    self.parent.canvas.winfo_height()
                                    - self.parent.canvas.image.height()
                                )
                                // 2
                                + self.parent.canvas.coords(self.parent.oval)[1]
                                + 5
                            )
                            / self.parent.canvas.image.height()
                            - height
                        ),
                    )
                )

                self.focuspoint = [
                    reference.axis[self.half][
                        np.abs(
                            np.asarray(reference.axis[self.half] - self.focuspoint[0])
                        ).argmin()
                    ],
                    reference.dose[self.half][
                        np.abs(
                            np.asarray(reference.dose[self.half] - self.focuspoint[1])
                        ).argmin()
                    ],
                ]

            except AttributeError:
                self.focuspoint = [
                    reference.axis[self.half][len(reference.axis[self.half]) // 2],
                    reference.dose[self.half][len(reference.dose[self.half]) // 2],
                ]
            except IndexError:
                self.focuspoint = [
                    reference.axis[self.half][len(reference.axis[self.half]) // 2],
                    reference.dose[self.half][len(reference.dose[self.half]) // 2],
                ]

            pixels = self.transform.transform(
                np.vstack([reference.axis[self.half], reference.dose[self.half]]).T
            )
            x, y = pixels.T
            y = height - y

            # Index of point closest to the double clicked point on the screen
            if self.norm == False:
                dist = np.argmin(
                    [
                        np.sqrt(
                            (
                                (reference.axis[self.half][i] - self.focuspoint[0])
                                / max(reference.axis[self.half])
                            )
                            ** 2
                            + (
                                (reference.dose[self.half][i] - self.focuspoint[1])
                                / max(reference.dose[self.half])
                            )
                            ** 2
                        )
                        for i in range(len(reference.axis[self.half]))
                    ]
                )
            else:
                dist = np.argmin(
                    [
                        np.sqrt(
                            (
                                (reference.axis[self.half][i] - self.focuspoint[0])
                                / max(reference.axis[self.half])
                            )
                            ** 2
                            + (
                                (
                                    reference.dose[self.half][i]
                                    * reference.normpoint
                                    / max(reference.dose[self.half])
                                    - self.focuspoint[1]
                                )
                                / (max(reference.dose[self.half]) / reference.normpoint)
                            )
                            ** 2
                        )
                        for i in range(len(reference.axis[self.half]))
                    ]
                )
            self.focuspoint = [
                reference.axis[self.half][dist],
                reference.dose[self.half][dist],
            ]
            self.pixelx = x[dist] / width
            self.pixely = y[dist] / height

            loc = "lower left"
            if self.half == False and self.plots[0].direction != "Z":
                if self.ax.get_xlim()[1] > 30:
                    loc = "lower center"

            self.axins = inset_axes(self.ax, "28%", "28%", loc=loc)
            if self.parent.dark.get() == True:
                self.axins.set_facecolor("#363636")

            self.axins.xaxis.label.set_color(self.textcolor)
            self.axins.yaxis.label.set_color(self.textcolor)

            self.axins.tick_params(axis="x", colors=self.textcolor)
            self.axins.tick_params(axis="y", colors=self.textcolor)

            self.axins.spines["left"].set_color(self.textcolor)
            self.axins.spines["bottom"].set_color(self.textcolor)

            yvalsat195 = []
            yvalsat205 = []
            for index, plot_data in enumerate(self.data):
                if self.errorbars == True:
                    try:
                        self.axins.errorbar(
                            x=plot_data[0],
                            y=plot_data[2],
                            yerr=plot_data[3],
                            fmt="none",
                            ecolor=self.colors[index],
                            elinewidth=0.625,
                            capsize=1.25,
                            capthick=0.25,
                            ms=2.5,
                        )
                    except ValueError:
                        pass
                self.axins.plot(
                    plot_data[0],
                    plot_data[2],
                    self.marker[index],
                    markersize=self.markersize,
                    color=self.colors[index],
                    linewidth=self.linewidth,
                    label=f"{self.plots[index].filename}",
                )
                yvalsat195 += [
                    plot_data[2][
                        plot_data[0].index(
                            min(
                                plot_data[0],
                                key=lambda x: abs(x - (self.focuspoint[0] - 5)),
                            )
                        )
                    ]
                ]
                yvalsat205 += [
                    plot_data[2][
                        plot_data[0].index(
                            min(
                                plot_data[0],
                                key=lambda x: abs(x - (self.focuspoint[0] + 5)),
                            )
                        )
                    ]
                ]

            # sub region of the original image
            x1, x2, y1, y2 = (
                self.focuspoint[0] - 5,
                self.focuspoint[0] + 5,
                0.95 * min(min(yvalsat195), min(yvalsat205)),
                1.05 * max(max(yvalsat195), max(yvalsat205)),
            )
            loc1 = 2
            loc2 = 4

            if y2 < y1:
                y1, y2 = y2, y1
                loc1, loc2 = 1, 3

            if self.half == True:
                x1, x2 = x1 + 3, x2 - 3

            self.axins.set_xlim(x1, x2)
            self.axins.set_ylim(y1, y2)
            self.axins.tick_params(
                labelleft=False,
                labelright=True,
                labelbottom=False,
                labeltop=True,
                bottom=False,
                left=False,
            )

            mark_inset(self.ax, self.axins, loc1=loc1, loc2=loc2, fc="none", ec="0.5")

        return

    def set_xlims(self):

        if self.parent.current_limits == []:
            self.current_limits = [self.ax.get_xlim()[0], self.ax.get_xlim()[1]]
            self.parent.current_limits = self.current_limits
            self.parent.initial_limits = self.current_limits
            self.parent.slidervars[0].set(self.current_limits[0])
            self.parent.slidervars[1].set(self.current_limits[1])

        self.current_limits = [
            self.parent.slidervars[0].get(),
            self.parent.slidervars[1].get(),
        ]

        self.ax.set_xlim(self.current_limits)

    def gamma(self):

        min_dose_percent = (
            int(
                min(self.data[1][2][int(len(self.data[1][2]) // 2) :])
                / max(self.data[1][2])
                * 100
            )
            + 1
        )

        if min_dose_percent < 20:
            min_dose_percent = 20

        gamma = pymedphys.gamma(
            (self.data[0][0],),
            self.data[0][2],
            (self.data[1][0],),
            self.data[1][2],
            self.parent.gammathreshold,
            self.parent.gammadist,
            quiet=True,
            lower_percent_dose_cutoff=min_dose_percent,
        )

        valid_gamma = gamma[~np.isnan(gamma)]
        pass_ratio = np.sum(valid_gamma <= 1) / len(valid_gamma)

        mb.showinfo(
            "Gamma-Index",
            f"?? ({self.parent.gammaacc.get()}) = {round(pass_ratio,4)}\n??? = {round(np.average(valid_gamma),4)}",
        )

    def return_figure(self, filenames):

        """Passes the image of the plot and the plot type to the MainApplication
        """
        try:
            plt.close(self.fig)
        except AttributeError:
            pass

        self.half = self.parent.half.get()
        try:
            self.add_plot_data(filenames)
            self.difference_plot()
        except IndexError:
            self.parent.filenames.pop(-1)
            return
        self.set_axis()
        self.set_x_label()
        self.fig.suptitle(self.title, fontsize=16)
        self.create_plots_from_data()
        if self.calcparams == True:
            try:
                self.add_descriptors()
            except Exception as e:
                self.parent.calcparams.set(False)
                self.calcparams = False
                sd.messagebox.showwarning("", self.text.calcfail[self.lang])

        self.add_legend()
        self.ax.set_aspect("auto")

        if self.half == True:

            xlim_r = [plots.axis[self.half] for plots in self.plots]
            xlim_r = max([item for sublist in xlim_r for item in sublist])
            self.ax.set_xlim(0, xlim_r)

        self.canvas.draw()
        buffer = self.canvas.buffer_rgba()
        image_array = np.asarray(buffer)
        fit_array = self.fits(image_array)
        image = Image.fromarray(fit_array)
        photoimage = ImageTk.PhotoImage(image)

        return photoimage, self.data[0][1]
