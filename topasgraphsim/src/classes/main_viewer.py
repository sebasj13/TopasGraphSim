import os
import time
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
from tkinter.colorchooser import askcolor

import pynput
from PIL import Image, ImageTk

from ..resources.info import show_info
from ..resources.language import Text
from .dose_figure_handler import DoseFigureHandler
from .profile import ProfileHandler
from .table import SimpleTable
from .xrangeslider import XRangeSlider


class MainApplication(tk.Frame):
    def __init__(self, parent):

        tk.Frame.__init__(self, parent)
        self.starttime = time.time()

        self.parent = parent

        self.logocanvas = tk.Canvas(self)
        self.logocanvas.pack(side=tk.TOP, fill="both", expand=True)
        self.center = [
            (self.winfo_screenwidth() // 2 + 50) // 2,
            (self.parent.winfo_screenheight() // 2) // 2,
        ]
        self.logo = ImageTk.PhotoImage(
            Image.open(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "..",
                    "resources",
                    "icon.png",
                )
            ).resize(
                (self.parent.minsize()[0] // 4, (self.parent.minsize()[0] // 4)),
                Image.LANCZOS,
            ),
            master=self.logocanvas,
        )
        self.logo_on_canvas = self.logocanvas.create_image(
            self.center[0], self.center[1], anchor=tk.CENTER, image=self.logo,
        )
        self.logocanvas.image = self.logo
        self.logocanvas.itemconfig(self.logo_on_canvas, image=self.logocanvas.image)

        self.parent.protocol("WM_DELETE_WINDOW", lambda: self.save_graph(True))

        # Read settings from profile.json and initialize the necessary variables
        self.direction = None
        self.saved = True
        self.menuflag = False
        self.xlimmenu = False
        self.canvas = tk.Canvas(self)
        self.photoimage = None
        self.image_on_canvas = None
        self.canvas.image = None
        self.current_file = None
        self.filenames = []
        self.rename_boxes = []
        self.new_limits = []
        self.current_event_width = -1
        self.current_event_height = -1

        self.profile = ProfileHandler()
        self.lang = self.profile.get_attribute("language")

        self.langvar = tk.StringVar()
        self.langvar.set(self.lang)
        self.text = Text()

        self.autostartdark = tk.StringVar()
        self.autostartdark.set(self.profile.get_attribute("color_scheme"))

        self.dark = tk.BooleanVar()
        self.dark.set(False)

        self.norm = tk.BooleanVar()
        self.norm.set(bool(self.profile.get_attribute("normalize")))

        self.errorbars = tk.BooleanVar()
        self.errorbars.set(True)

        self.caxcorrection = tk.BooleanVar()
        self.caxcorrection.set(False)

        self.diffplot = tk.BooleanVar()
        self.diffplot.set(False)

        self.zoom = tk.BooleanVar()
        self.zoom.set(bool(self.profile.get_attribute("zoom")))

        self.half = tk.BooleanVar()
        self.half.set(bool(self.profile.get_attribute("halfview")))

        self.calcparams = tk.BooleanVar()
        self.calcparams.set(False)

        self.tablevar = tk.BooleanVar()
        self.tablevar.set(False)

        self.fullscreen = tk.BooleanVar()
        self.fullscreen.set(bool(self.profile.get_attribute("fullscreen")))

        self.axlims = tk.IntVar()
        self.axlims.set(0)

        self.normvaluemenu = tk.StringVar()
        self.normvaluemenu.set("max")

        self.errlimval = tk.StringVar()
        self.errlimval.set("absolute")

        self.slidervars = [tk.DoubleVar(), tk.DoubleVar()]
        self.current_limits = []
        self.initial_limits = []

        self.DoseFigureHandler = DoseFigureHandler(self)

        # Keybinding definitions
        self.parent.bind("<Configure>", self.handle_configure)
        self.parent.bind("<Control-e>", lambda type: self.load_file("egs"))
        self.parent.bind("<Control-d>", lambda type: self.load_file("dp"))
        self.parent.bind("<Control-o>", lambda type: self.load_file("simulation"))
        self.parent.bind("<Control-s>", self.save_graph)
        self.parent.bind("<Control-t>", lambda type: self.load_file("pdd"))
        self.parent.bind("<Control-p>", lambda type: self.load_file("ptw"))
        self.parent.bind("<Escape>", self.close_file)
        self.parent.bind("<Control-z>", self.remove_last_addition)
        self.parent.bind("<F11>", self.toggle_fullscreen)
        self.parent.bind("<MouseWheel>", self.change_x_limits)
        self.parent.bind(
            "<Control-Alt-Up>", lambda boolean1: self.change_errlims(True, True)
        )
        self.parent.bind(
            "<Control-Alt-Down>", lambda boolean1: self.change_errlims(True, False),
        )
        self.parent.bind(
            "<Control-Shift-Up>", lambda boolean1: self.change_errlims(False, True),
        )
        self.parent.bind(
            "<Control-Shift-Down>", lambda boolean1: self.change_errlims(False, False),
        )
        self.parent.bind("<Control-Up>", lambda boolean: self.change_marker_size(True))
        self.parent.bind(
            "<Control-Down>", lambda boolean: self.change_marker_size(False)
        )

        self.parent.bind(
            "<Control-Right>", lambda boolean: self.change_line_width(True)
        )
        self.parent.bind(
            "<Control-Left>", lambda boolean: self.change_line_width(False)
        )

        # Menubar definitions

        self.menubar = tk.Menu(self.parent, tearoff=False)
        self.filemenu = tk.Menu(self.menubar, tearoff=False)
        self.addmeasuremenu = tk.Menu(self.menubar, tearoff=False)
        self.addmeasuremenu.add_command(
            label=self.text.pdd[self.lang],
            command=lambda: self.load_file("pdd"),
            accelerator="Ctrl+T",
        )
        self.addmeasuremenu.add_command(
            label=self.text.dp[self.lang],
            command=lambda: self.load_file("dp"),
            accelerator="Ctrl+D",
        )
        self.addmeasuremenu.add_command(
            label=self.text.ptw[self.lang],
            command=lambda: self.load_file("ptw"),
            accelerator="Ctrl+P",
        )

        self.addsimmenu = tk.Menu(self.menubar)

        self.addsimmenu.add_command(
            label="TOPAS",
            command=lambda: self.load_file("simulation"),
            accelerator="Ctrl+O",
        )
        self.addsimmenu.add_command(
            label="3Ddose", command=lambda: self.load_file("egs"), accelerator="Ctrl+E",
        )

        self.filemenu.add_cascade(
            label=self.text.loadsim[self.lang], menu=self.addsimmenu
        )
        self.filemenu.add_cascade(
            label=self.text.loadmeasurement[self.lang], menu=self.addmeasuremenu
        )
        self.filemenu.add_separator()
        self.filemenu.add_command(
            label=self.text.save[self.lang],
            command=self.save_graph,
            accelerator="Ctrl+S",
        )
        self.filemenu.add_command(
            label=self.text.close[self.lang],
            command=self.close_file,
            accelerator="Esc",
        )
        self.filemenu.add_separator()
        self.filemenu.add_command(
            label=self.text.end[self.lang], command=lambda: self.save_graph(True)
        )
        self.filemenu.entryconfig(3, state=tk.DISABLED)
        self.filemenu.entryconfig(4, state=tk.DISABLED)
        self.addmenu = tk.Menu(self.menubar, tearoff=False)
        self.addmenu.add_cascade(
            label=self.text.simulation[self.lang], menu=self.addsimmenu
        )
        self.addmenu.add_cascade(
            label=self.text.measurement[self.lang], menu=self.addmeasuremenu
        )
        self.addmenu.add_separator()
        self.addmenu.add_command(
            label=self.text.revert[self.lang],
            command=self.remove_last_addition,
            accelerator="Ctrl+Z",
        )
        self.addmenu.entryconfig(3, state=tk.DISABLED)
        self.menubar.add_cascade(label=self.text.file[self.lang], menu=self.filemenu)
        self.viewmenu = tk.Menu(self.menubar, tearoff=False)
        self.viewmenu.add_checkbutton(
            label=self.text.light[self.lang],
            variable=self.dark,
            command=lambda: self.switchtheme("light"),
            onvalue=0,
            offvalue=1,
        )
        self.viewmenu.add_checkbutton(
            label=self.text.dark[self.lang],
            variable=self.dark,
            command=lambda: self.switchtheme("dark"),
            onvalue=1,
            offvalue=0,
        )

        self.viewmenu.add_checkbutton(
            label=self.text.fullscreen[self.lang],
            variable=self.fullscreen,
            command=self.toggle_fullscreen,
            onvalue=1,
            offvalue=0,
            accelerator="F11",
        )

        self.menubar.add_cascade(label=self.text.view[self.lang], menu=self.viewmenu)
        self.optionsmenu = tk.Menu(self.menubar, tearoff=False)
        self.optionsmenu.add_checkbutton(
            label=self.text.startdark[self.lang],
            variable=self.autostartdark,
            command=lambda: self.profile.set_attribute(
                "color_scheme", f"{self.autostartdark.get()}"
            ),
            onvalue="dark",
            offvalue="light",
        )
        self.langmenu = tk.Menu(self.menubar, tearoff=False)
        self.langmenu.add_radiobutton(
            label=self.text.german[self.lang],
            command=lambda: self.set_language(self.langvar.get()),
            variable=self.langvar,
            value="de",
        )
        self.langmenu.add_radiobutton(
            label=self.text.english[self.lang],
            command=lambda: self.set_language(self.langvar.get()),
            variable=self.langvar,
            value="en",
        )
        self.optionsmenu.add_cascade(
            label=self.text.language[self.lang], menu=self.langmenu
        )
        self.menubar.add_cascade(
            label=self.text.options[self.lang], menu=self.optionsmenu
        )

        self.normmenu = tk.Menu(self.menubar, tearoff=False)

        self.markersizemenu = tk.Menu(self.menubar, tearoff=False)
        self.markersizemenu.add_command(
            label=Text().increase[self.lang],
            command=lambda: self.change_marker_size(True),
            accelerator="Ctrl + ↑",
        )

        self.markersizemenu.add_command(
            label=Text().decrease[self.lang],
            command=lambda: self.change_marker_size(False),
            accelerator="Ctrl + ↓",
        )

        self.markerlinemenu = tk.Menu(self.menubar, tearoff=False)
        self.markerlinemenu.add_command(
            label=Text().increase[self.lang],
            command=lambda: self.change_line_width(True),
            accelerator="Ctrl + →",
        )

        self.markerlinemenu.add_command(
            label=Text().decrease[self.lang],
            command=lambda: self.change_line_width(False),
            accelerator="Ctrl + ←",
        )

        self.normmenu.add_cascade(
            label=Text().markerline[self.lang], menu=self.markerlinemenu
        )
        self.normmenu.add_cascade(
            label=Text().marker[self.lang], menu=self.markersizemenu
        )

        self.normmenu.add_command(
            label=self.text.resetcolors[self.lang], command=self.reset_colors
        )

        self.normmenu.add_separator()

        self.normalizemenu = tk.Menu(self.menubar, tearoff=False)
        self.normalizemenu.add_checkbutton(
            label=self.text.normalize[self.lang],
            command=self.normalize,
            variable=self.norm,
        )
        self.normalize_cascade = tk.Menu(self.menubar, tearoff=False)
        self.normalize_cascade.add_radiobutton(
            label=self.text.maximum[self.lang],
            variable=self.normvaluemenu,
            value="max",
            command=self.change_normalization,
        )
        self.normalize_cascade.add_radiobutton(
            label=self.text.flank[self.lang],
            variable=self.normvaluemenu,
            value="flank",
            command=self.change_normalization,
        )
        self.normalize_cascade.add_radiobutton(
            label=self.text.centeraxis[self.lang],
            variable=self.normvaluemenu,
            value="center",
            command=self.change_normalization,
        )
        self.normalizemenu.add_cascade(
            label=self.text.choosenormalization[self.lang], menu=self.normalize_cascade
        )

        self.normmenu.add_cascade(
            label=self.text.normalization[self.lang], menu=self.normalizemenu
        )
        self.normmenu.add_checkbutton(
            label=self.text.errorbars[self.lang],
            command=self.show_errorbars,
            variable=self.errorbars,
        )
        self.normmenu.add_checkbutton(
            label=self.text.zoom[self.lang], command=self.zoomgraph, variable=self.zoom,
        )

        self.normmenu.add_checkbutton(
            label=self.text.half[self.lang], command=self.halfgraph, variable=self.half,
        )
        self.normmenu.add_separator()

        self.parammenu = tk.Menu(self.menubar, tearoff=False)
        self.parammenu.add_checkbutton(
            label=self.text.adddescriptors[self.lang],
            command=self.calculate_parameters,
            variable=self.calcparams,
        )
        self.parammenu.add_checkbutton(
            label=self.text.showtable[self.lang],
            command=self.show_table,
            variable=self.tablevar,
        )

        self.normmenu.add_cascade(
            label=self.text.calcparams[self.lang], menu=self.parammenu
        )

        self.normmenu.add_checkbutton(
            label=self.text.caxcorrection[self.lang],
            command=self.correct_caxdev,
            variable=self.caxcorrection,
        )
        self.normmenu.add_separator()
        self.normmenu.add_checkbutton(
            label=self.text.differenceplot[self.lang],
            command=self.differenceplot,
            variable=self.diffplot,
        )

        self.normmenu.entryconfig(12, state=tk.DISABLED)

        self.errlimmenu = tk.Menu(self.menubar, tearoff=False)
        self.errlimmenu.add_command(
            label=Text().increaseupper[self.lang],
            command=lambda: self.change_errlims(True, True),
            accelerator="Ctrl + +",
        )

        self.errlimmenu.add_command(
            label=Text().decreaseupper[self.lang],
            command=lambda: self.change_errlims(True, False),
            accelerator="Ctrl + -",
        )
        self.errlimmenu.add_command(
            label=Text().increselower[self.lang],
            command=lambda: self.change_errlims(False, True),
            accelerator="Ctrl + Alt + +",
        )
        self.errlimmenu.add_command(
            label=Text().decreaselower[self.lang],
            command=lambda: self.change_errlims(False, False),
            accelerator="Ctrl + Alt + -",
        )

        self.errlimvalmenu = tk.Menu(self.menubar, tearoff=False)
        self.errlimvalmenu.add_radiobutton(
            label=self.text.percentage[self.lang],
            variable=self.errlimval,
            value="percentage",
            command=self.changeerrdisplay,
        )
        self.errlimvalmenu.add_radiobutton(
            label=self.text.absolute[self.lang],
            variable=self.errlimval,
            value="absolute",
            command=self.changeerrdisplay,
        )

        self.errlimmenu.add_cascade(
            label=self.text.changeerr[self.lang], menu=self.errlimvalmenu
        )

        self.normmenu.add_cascade(
            label=Text().errlimmenu[self.lang], menu=self.errlimmenu
        )
        self.normmenu.entryconfig(13, state=tk.DISABLED)

        self.menubar.add_command(label=self.text.about[self.lang], command=self.about)

        self.parent.config(menu=self.menubar)

        self.parent.title(self.text.window_title[self.lang])

        self.pack(side="top", fill="both", expand=True)
        self.frame2 = tk.Frame(self.parent, bg="red")

        self.parent.attributes("-fullscreen", self.fullscreen.get())
        self.autostart()

    def about(self):
        show_info(self.parent, self.lang, self.dark.get())

    def autostart(self):

        """Sets the theme according to the profile.json
        """

        if self.autostartdark.get() == "light":
            self.dark.set(False)
            self.switchtheme("light")
        else:
            self.dark.set(True)
            self.switchtheme("dark")

        return

    def switchtheme(self, theme):

        """Switches between light and dark theme
        """

        if theme == "light":
            self.parent.tk.call("set_theme", "light")
            self.logocanvas.configure(background="#ffffff")
            self.parent.configure(background="#ffffff")

        else:
            # Set dark theme
            self.parent.tk.call("set_theme", "dark")
            self.parent.configure(background="#363636")
            self.logocanvas.configure(background="#333333")

        if self.filenames != []:
            self.logocanvas.pack_forget()
            self.show_preview()

        return

    def toggle_fullscreen(self, event=None):

        """Toggle between fullscreen and normal view
        """

        self.parent.attributes("-fullscreen", not self.parent.attributes("-fullscreen"))
        self.fullscreen.set(self.parent.attributes("-fullscreen"))
        self.profile.set_attribute("fullscreen", bool(self.fullscreen.get()))

    def change_x_limits(self, event=None):

        if event.delta > 0:

            if self.DoseFigureHandler.plots[0].direction == "Z":
                self.slidervars[1].set(self.slidervars[1].get() - 5)
            else:

                if self.slidervars[0].get() >= 0:
                    self.slidervars[0].set(self.slidervars[0].get() - 5)
                else:
                    self.slidervars[0].set(self.slidervars[0].get() + 5)

                if self.slidervars[1].get() >= 0:
                    self.slidervars[1].set(self.slidervars[1].get() - 5)
                else:
                    self.slidervars[1].set(self.slidervars[1].get() + 5)
        elif event.delta < 0:

            if self.DoseFigureHandler.plots[0].direction == "Z":
                self.slidervars[1].set(self.slidervars[1].get() + 5)
            else:

                if self.slidervars[0].get() >= 0:
                    self.slidervars[0].set(self.slidervars[0].get() + 5)
                else:
                    self.slidervars[0].set(self.slidervars[0].get() - 5)

                if self.slidervars[1].get() >= 0:
                    self.slidervars[1].set(self.slidervars[1].get() + 5)
                else:
                    self.slidervars[1].set(self.slidervars[1].get() - 5)

        self.current_limits = [self.slidervars[0].get(), self.slidervars[1].get()]

        self.show_preview()

        return

    def change_xrange(self):

        self.parent.unbind("<MouseWheel>")
        for i, var in enumerate(self.initial_limits):
            if var < 0 and var < self.current_limits[i]:
                self.current_limits[i] = var

            if var >= 0 and var > self.current_limits[i]:
                self.current_limits[i] = var

        self.xlimmenu = True
        self.slider = XRangeSlider(self, self.slidervars, self.current_limits)

        return

    def set_language(self, language):

        """Sets the desired language and reinitiates the program
        """

        plots = self.DoseFigureHandler.plots
        filenames = self.filenames
        dark = self.dark.get()
        axlims = self.axlims.get()
        calcparams = self.calcparams.get()
        caxcorrection = self.caxcorrection.get()
        normalize = self.norm.get()
        errorbars = self.errorbars.get()
        diffplot = self.diffplot.get()
        errlimmin = self.DoseFigureHandler.errlimmin
        errlimmax = self.DoseFigureHandler.errlimmax
        initial_limits = self.initial_limits
        current_limits = [self.slidervars[0].get(), self.slidervars[1].get()]
        table = self.tablevar.get()
        dark = self.dark.get()
        try:
            self.slider.submit()
            self.slider.window.destroy()
            self.slider = None
        except Exception:
            pass
        self.pack_forget()
        self.parent.config(menu=None)
        self.profile.set_attribute("language", language)
        self.__init__(self.parent)
        if plots != []:
            self.filenames = filenames
            self.DoseFigureHandler.plots = plots
            self.dark.set(dark)
            self.tablevar.set(table)
            self.axlims.set(axlims)
            self.calcparams.set(calcparams)
            self.caxcorrection.set(caxcorrection)
            self.norm.set(normalize)
            self.errorbars.set(errorbars)
            self.diffplot.set(diffplot)
            self.current_limits = current_limits
            self.initial_limits = initial_limits
            self.slidervars[0].set(self.current_limits[0])
            self.slidervars[1].set(self.current_limits[1])
            self.DoseFigureHandler.diffplot = diffplot
            self.DoseFigureHandler.errlimmin = errlimmin
            self.DoseFigureHandler.errlimmax = errlimmax
            if dark == True:
                self.switchtheme("dark")
                self.dark.set(True)
            else:
                self.switchtheme("light")
                self.dark.set(False)
            self.show_preview()
            if table == True:
                if self.direction != "Z":
                    self.table.set(0, 1, self.text.fwhm[self.lang], self.fontsize)

        return

    def load_file(self, type, event=None):

        """Loads measurement or simulation data to be displayed
        """

        if type == "simulation":
            filetypes = [(self.text.topas[self.lang], [".csv", ".bin"])]
        if type == "egs":
            filetypes = [(self.text.egs[self.lang], [".3ddose"])]
        elif type == "pdd" or type == "dp":
            filetypes = [(self.text.measurementdata[self.lang], ["txt", ".csv"])]
        elif type == "ptw":
            filetypes = [(self.text.ptw[self.lang], ".mcc")]
        self.current_file = fd.askopenfilenames(
            initialdir=os.getcwd(), filetypes=filetypes
        )

        if self.current_file == "" or self.current_file == ():
            return

        for file in self.current_file:
            self.filenames += [(file, type)]
        self.logocanvas.pack_forget()
        self.show_preview()
        self.filemenu.entryconfig(0, state=tk.DISABLED)
        self.filemenu.entryconfig(1, state=tk.DISABLED)
        self.filemenu.entryconfig(3, state=tk.NORMAL)
        self.filemenu.entryconfig(4, state=tk.NORMAL)
        if len(self.filenames) > 2:
            self.normmenu.entryconfig(12, state=tk.DISABLED)
        self.saved = False

        return

    def load_dropped_file(self, files):
        """Loads measurement or simulation data to be displayed
        """

        for i, character in enumerate(files):
            if character == " ":
                if files[i + 1] == "{":
                    files = files[:i] + ";" + files[i + 1 :]
                else:
                    if files[:i].count("{") == files[:i].count("}"):
                        files = files[:i] + ";" + files[i + 1 :]

        files = files.split(";")
        for i, file in enumerate(files):
            if "{" in file:
                files[i] = file[1:-1]

        types = {
            "csv": "simulation",
            "3ddose": "egs",
            "bin": "simulation",
            "mcc": "ptw",
        }
        extensions = []
        for i, file in enumerate(files):
            try:
                extensions += [types[file.split(".")[-1]]]
            except KeyError:
                files.pop(i)

        self.current_file = files

        for i, file in enumerate(self.current_file):
            self.filenames += [(file, extensions[i])]

        if len(self.filenames) == 0:
            return

        self.logocanvas.pack_forget()
        self.show_preview()
        self.filemenu.entryconfig(0, state=tk.DISABLED)
        self.filemenu.entryconfig(1, state=tk.DISABLED)
        self.filemenu.entryconfig(3, state=tk.NORMAL)
        self.filemenu.entryconfig(4, state=tk.NORMAL)
        if len(self.filenames) > 2:
            self.normmenu.entryconfig(12, state=tk.DISABLED)
        self.saved = False

    def close_file(self, event=None):

        """Closes the current project
        """
        self.canvas.pack_forget()
        self.filemenu.entryconfig(0, state=tk.NORMAL)
        self.filemenu.entryconfig(1, state=tk.NORMAL)
        self.filemenu.entryconfig(3, state=tk.DISABLED)
        self.filemenu.entryconfig(4, state=tk.DISABLED)
        self.addmenu.entryconfig(0, state=tk.NORMAL)
        self.addmenu.entryconfig(1, state=tk.NORMAL)
        self.addmeasuremenu.entryconfig(0, state=tk.NORMAL)
        self.addmeasuremenu.entryconfig(1, state=tk.NORMAL)
        self.normmenu.entryconfig(12, state=tk.DISABLED)
        self.normmenu.entryconfig(13, state=tk.DISABLED)
        self.parammenu.entryconfig(0, state=tk.NORMAL)
        self.menubar.delete(4, 5)
        self.filenames = []
        try:
            self.canvas.itemconfig(self.image_on_canvas, image=None)
        except Exception:
            pass
        self.DoseFigureHandler.plots = []
        self.diffplot.set(False)
        self.DoseFigureHandler.diffplot = False
        self.DoseFigureHandler.xaxisname == None
        self.direction = None
        self.errlimmin = 1.1
        self.errlimmax = 1.1
        self.saved = True
        self.menuflag = False
        self.current_limits = []
        self.initial_limits = []
        self.rename_boxes = []
        self.slidervars = [tk.DoubleVar(), tk.DoubleVar()]
        self.DoseFigureHandler.caxcorrection = False
        self.caxcorrection.set(False)
        try:
            self.slider.window.destroy()
            self.xlimmenu = False
        except AttributeError:
            pass
        try:
            self.table.pack_forget()
            self.tablevar.set(False)
        except AttributeError:
            pass
        deltax = self.winfo_width() // 2 - self.center[0]
        deltay = self.winfo_height() // 2 - self.center[1]
        self.center = [self.winfo_width() // 2, self.winfo_height() // 2]
        self.logocanvas.move(self.logo_on_canvas, deltax, deltay)
        self.logocanvas.pack(side=tk.TOP, fill="both", expand=True)
        return

    def save_graph(self, exit=False):

        """Saves the current graph as an image
        """

        try:
            self.slider.submit()
            self.slider.window.destroy()
            self.slider = None
        except Exception:
            pass

        if exit == True:
            if self.saved == False:

                prompt = sd.messagebox.askyesno("", self.text.closeprompt[self.lang])
                if prompt == True:
                    self.parent.destroy()
                    return
                else:
                    return
            else:
                self.parent.destroy()
                return

        file = fd.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                (self.text.image[self.lang], [".png", ".jpg"]),
                ("PDF", [".pdf"]),
            ],
        )

        if file is None:
            return

        ImageTk.getimage(self.photoimage).convert("RGB").save(file)
        self.saved = True

        return

    def normalize(self):

        """Choose whether or not the displayed graph should be normalized
        """

        self.DoseFigureHandler.norm = self.norm.get()

        self.profile.set_attribute("normalize", int(self.norm.get()))
        self.refresh()

        return

    def show_errorbars(self):

        """Choose whether or not the displayed graph should be contain errorbars
        """

        self.DoseFigureHandler.errorbars = self.errorbars.get()

        self.refresh()

        return

    def correct_caxdev(self):

        """Choose whether or not the displayed dose
        profiles should be center-axis-corrected
        """

        self.DoseFigureHandler.caxcorrection = self.caxcorrection.get()

        self.refresh()

        return

    def calculate_parameters(self):

        """Choose whether or not the displayed dose
        profiles should be center-axis-corrected
        """

        self.DoseFigureHandler.calcparams = self.calcparams.get()

        self.refresh()

        return

    def show_table(self):

        self.calcparams.set(False)
        if self.tablevar.get() == False:
            self.table.destroy()
            del self.table
        else:
            self.add_table()

        self.refresh()

        return

    def remove_last_addition(self, event=None):

        """
        Removes the graph added last
        """

        if len(self.filenames) == 1:
            self.close_file()
            return

        if len(self.filenames) == 2:
            self.diffplot.set(False)
            self.DoseFigureHandler.diffplot = False
            self.normmenu.entryconfig(12, state=tk.DISABLED)

        if self.filenames[-1][0].endswith(".mcc") == True:
            self.filenames.pop(-1)
            while len(self.filenames) < len(self.DoseFigureHandler.plots):
                self.DoseFigureHandler.plots.pop(-1)

        else:
            self.filenames.pop(-1)
            self.DoseFigureHandler.plots.pop(-1)

        if len(self.filenames) <= 4:
            self.addmenu.entryconfig(0, state=tk.NORMAL)
            self.addmenu.entryconfig(1, state=tk.NORMAL)
            self.parammenu.entryconfig(0, state=tk.NORMAL)

        self.canvas.itemconfig(self.image_on_canvas, image=None)
        self.show_preview()

        return

    def change_normalization(self):

        """Change the normalization to different points
        """

        if self.normvaluemenu.get() == "max":
            self.DoseFigureHandler.normvalue = "max"
        elif self.normvaluemenu.get() == "flank":
            self.DoseFigureHandler.normvalue = "flank"
        else:
            self.DoseFigureHandler.normvalue = "center"

        self.refresh()

        return

    def differenceplot(self):

        self.DoseFigureHandler.diffplot = self.diffplot.get()
        if self.diffplot.get() == True:
            self.normmenu.entryconfig(13, state=tk.NORMAL)
        else:
            self.normmenu.entryconfig(13, state=tk.DISABLED)

        self.refresh()

        return

    def change_errlims(self, boolean1, boolean2):
        if boolean1 == True:
            if boolean2 == True:
                self.DoseFigureHandler.errlimmax += 0.5
            else:
                self.DoseFigureHandler.errlimmax -= 0.5
        else:
            if boolean2 == True:
                self.DoseFigureHandler.errlimmin -= 0.5
            else:
                self.DoseFigureHandler.errlimmin += 0.5

        self.refresh()

    def changeerrdisplay(self):

        self.prev_difference = self.DoseFigureHandler.difference

        if self.errlimval.get() == "percentage":
            self.DoseFigureHandler.errlimval = "percentage"
            self.DoseFigureHandler.errlimmax = 1.1
        else:
            self.DoseFigureHandler.errlimval = "absolute"

        self.refresh()

    def zoomgraph(self):

        """Choose whether or not the displayed graph
        should contain inset axis for a zoom view
        """

        self.DoseFigureHandler.zoom = self.zoom.get()

        self.profile.set_attribute("zoom", int(self.zoom.get()))

        self.refresh()

        return

    def halfgraph(self):

        """Choose whether or not to only show half of the dose profile
        """

        self.DoseFigureHandler.half = self.half.get()
        self.profile.set_attribute("halfview", self.half.get())
        self.show_preview()

        return

    def change_marker_size(self, boolean, event=None):

        """Change the size of the matplotlib markers in the graph
        """

        if boolean == True:
            self.DoseFigureHandler.markersize += 0.2
        else:
            self.DoseFigureHandler.markersize -= 0.2

        if self.DoseFigureHandler.markersize < 0:
            self.DoseFigureHandler.markersize = 0

        self.profile.set_attribute("markersize", self.DoseFigureHandler.markersize)

        self.refresh()

        return

    def change_line_width(self, boolean, event=None):

        """Change the width of the matplotlib lines in the graph
        """

        if boolean == True:
            self.DoseFigureHandler.linewidth += 0.2
        else:
            self.DoseFigureHandler.linewidth -= 0.2
        if self.DoseFigureHandler.linewidth < 0.2:
            self.DoseFigureHandler.linewidth = 0.2

        self.profile.set_attribute("linewidth", self.DoseFigureHandler.linewidth)

        self.refresh()
        return

    def reset_colors(self):
        self.profile.set_attribute(
            "colors", self.profile.get_attribute("default_colors")
        )
        self.DoseFigureHandler.colors = self.profile.get_attribute("default_colors")
        self.show_preview()

    def show_preview(self):

        """
        Invokes DoseFigureHandler to create and display the graphs with the selected options
        """
        self.photoimage, self.direction = self.DoseFigureHandler.return_figure(
            self.filenames
        )

        self.logocanvas.pack_forget()
        self.canvas.pack_forget()
        self.canvas = tk.Canvas(self)
        self.canvas.bind("<Button-1>", self.check_click)
        self.canvas.bind("<Button-3>", self.check_right_click)
        self.canvas.bind("<Motion>", self.check_hand)
        self.canvas.bind("<Double-Button-1>", self.new_zoom)
        self.parent.bind("<Up>", lambda boolean: self.change_order(True))
        self.parent.bind("<Down>", lambda boolean: self.change_order(False))

        if len(self.DoseFigureHandler.plots) >= 2:
            self.addmenu.entryconfig(3, state=tk.NORMAL)
            self.normmenu.entryconfig(12, state=tk.DISABLED)

        if len(self.DoseFigureHandler.plots) == 2:
            self.normmenu.entryconfig(12, state=tk.NORMAL)

        if len(self.DoseFigureHandler.plots) > 5:
            self.parammenu.entryconfig(0, state=tk.DISABLED)

        if len(self.DoseFigureHandler.plots) == 10:
            self.addmenu.entryconfig(0, state=tk.DISABLED)
            self.addmenu.entryconfig(1, state=tk.DISABLED)
        if self.direction == "Z":
            self.addmeasuremenu.entryconfig(1, state=tk.DISABLED)
            self.normmenu.entryconfig(7, state=tk.DISABLED)
            self.normmenu.entryconfig(10, state=tk.DISABLED)
        else:
            self.addmeasuremenu.entryconfig(0, state=tk.DISABLED)
            self.normmenu.entryconfig(7, state=tk.NORMAL)
            self.normmenu.entryconfig(10, state=tk.NORMAL)

        if self.menuflag == False:
            self.menubar.add_cascade(label=self.text.add[self.lang], menu=self.addmenu)
            self.menubar.add_cascade(label="Graph", menu=self.normmenu)
            self.menuflag = True
        self.image_on_canvas = self.canvas.create_image(
            self.winfo_width() // 2,
            self.winfo_height() // 2,
            anchor=tk.CENTER,
            image=self.photoimage,
        )

        self.canvas.image = self.photoimage
        self.canvas.itemconfig(self.image_on_canvas, image=self.canvas.image)
        self.canvas.pack(side=tk.TOP, fill="both", expand=True)

        for i in range(len(self.DoseFigureHandler.plots)):
            normdiff = 0
            if self.norm.get() == True:
                normdiff = 0.035
            factor = (self.canvas.image.width() / self.canvas.image.height()) / 2
            temp = self.canvas.create_rectangle(
                (
                    -0.00833
                    * max(
                        map(
                            len,
                            [plot.filename for plot in self.DoseFigureHandler.plots],
                        )
                    )
                    + 0.94633
                )
                * self.canvas.image.width(),
                (0.023 + normdiff + 0.042 * i) * self.canvas.image.height() * factor,
                0.988 * self.canvas.image.width(),
                (0.065 + normdiff + 0.042 * i) * self.canvas.image.height() * factor,
                fill="",
                outline="",
                tags="rename",
            )
            self.rename_boxes += [temp]

        if self.zoom.get() == True:

            self.pixelx = self.DoseFigureHandler.pixelx
            self.pixely = self.DoseFigureHandler.pixely

            self.oval = self.canvas.create_oval(
                self.pixelx * self.canvas.image.width() - 5,
                self.pixely * self.canvas.image.height() - 5,
                self.pixelx * self.canvas.image.width() + 5,
                self.pixely * self.canvas.image.height() + 5,
                fill="",
                outline="",
                tags="token",
            )

    def add_table(self):
        try:
            if len(self.DoseFigureHandler.plots) == len(self.table._widgets[0]) - 1:
                return
        except AttributeError:
            pass
        try:

            self.fontsize = int(
                round(
                    9.333
                    + 6.6667
                    * (self.parent.winfo_width() / self.parent.winfo_screenwidth()),
                    0,
                )
            )

            if self.direction == "Z":
                self.table = SimpleTable(
                    self.parent, 4, len(self.DoseFigureHandler.plots) + 1
                )
                self.table.set(0, 0, self.text.metric[self.lang], self.fontsize)
                self.table.set(1, 0, "Q", self.fontsize)
                self.table.set(2, 0, "dQ", self.fontsize)
                self.table.set(3, 0, "z_max", self.fontsize)
                for i in range(1, len(self.DoseFigureHandler.plots) + 1):
                    self.table.set(0, i, "⬤", self.fontsize)
                    self.table._widgets[0][i].configure(
                        fg=self.DoseFigureHandler.colors[i - 1]
                    )
                for i in range(1, len(self.DoseFigureHandler.plots) + 1):
                    for j in range(1, 4):
                        self.table.set(
                            j,
                            i,
                            self.DoseFigureHandler.plots[i - 1].params()[j - 1],
                            self.fontsize,
                        )
                self.table.pack(side="bottom", fill="y", pady=(10, 2))
            else:
                self.table = SimpleTable(
                    self.parent, len(self.DoseFigureHandler.plots) + 1, 10
                )
                self.table.set(0, 0, self.text.metric[self.lang], self.fontsize)
                self.table.set(0, 1, self.text.fwhm[self.lang], self.fontsize)
                self.table.set(0, 2, "CAXdev", self.fontsize)
                self.table.set(0, 3, "flat_krieger", self.fontsize)
                self.table.set(0, 4, "flat_stddev", self.fontsize)
                self.table.set(0, 5, "S", self.fontsize)
                self.table.set(0, 6, "Lpenumbra", self.fontsize)
                self.table.set(0, 7, "Rpenumbra", self.fontsize)
                self.table.set(0, 8, "Lintegral", self.fontsize)
                self.table.set(0, 9, "Rintegral", self.fontsize)

                for i in range(1, len(self.DoseFigureHandler.plots) + 1):
                    self.table.set(i, 0, "⬤", self.fontsize)
                    self.table._widgets[i][0].configure(
                        fg=self.DoseFigureHandler.colors[i - 1]
                    )
                for i in range(1, len(self.DoseFigureHandler.plots) + 1):
                    for j in range(1, 10):
                        self.table.set(
                            i,
                            j,
                            self.DoseFigureHandler.plots[i - 1].params()[j - 1],
                            self.fontsize,
                        )
                        if self.caxcorrection.get() == True:
                            if j == 2:
                                self.table.set(
                                    i, j, "0.00", self.fontsize,
                                )

                self.table.pack(side="bottom", fill="both", padx=(2, 2), pady=(10, 2))
            self.table.configure(bg="black")
        except Exception as e:
            print(e)
            self.tablevar.set(False)
            sd.messagebox.showwarning("", self.text.calcfail[self.lang])

    def new_zoom(self, event):

        if self.zoom.get() == True:

            delta_x = event.x - self.canvas.coords(self.oval)[0] + 5
            delta_y = event.y - self.canvas.coords(self.oval)[1] + 5
            self.canvas.move(self.oval, delta_x, delta_y)
            self.show_preview()

    def change_order(self, boolean):

        if self.index != None:

            x = self.parent.winfo_pointerx()
            y = self.parent.winfo_pointery()

            factor = 1
            if self.DoseFigureHandler.plots[0].direction == "Z":
                factor = 6 / 5

            if boolean == True:

                new_index = self.index - 1
                dy = -0.035 * factor

                if self.index == 0:
                    new_index = len(self.rename_boxes) - 2
                    dy = 0.035 * factor * (len(self.rename_boxes) - 2)

            else:
                if self.index + 1 == len(self.rename_boxes) - 1:
                    new_index = 0
                    dy = -0.035 * factor * (len(self.rename_boxes) - 2)

                else:
                    new_index = self.index + 1
                    dy = 0.035 * factor

            (
                self.DoseFigureHandler.plots[self.index],
                self.DoseFigureHandler.plots[new_index],
            ) = (
                self.DoseFigureHandler.plots[new_index],
                self.DoseFigureHandler.plots[self.index],
            )
            (
                self.DoseFigureHandler.colors[self.index],
                self.DoseFigureHandler.colors[new_index],
            ) = (
                self.DoseFigureHandler.colors[new_index],
                self.DoseFigureHandler.colors[self.index],
            )
            self.profile.set_attribute("colors", self.DoseFigureHandler.colors)

            try:
                (self.filenames[self.index], self.filenames[new_index],) = (
                    self.filenames[new_index],
                    self.filenames[self.index],
                )
            except IndexError:
                pass

            factor = (
                1000 * self.parent.winfo_height() / self.parent.winfo_screenheight()
            )

            x = self.parent.winfo_pointerx()
            y = int(self.parent.winfo_pointery())
            y += dy * factor
            pynput.mouse.Controller().position = (x, y)
            self.index = new_index
            self.show_preview()
            self.canvas.config(cursor="hand1")
            return

    def refresh(self):

        if self.filenames != []:
            # self.canvas.itemconfig(self.image_on_canvas, image=None)
            self.show_preview()
        return

    def handle_configure(self, event=None):

        """
        Dynamically resizes the graph, rename boxes and zoom window selector
        according to the window size and name length
        """

        if type(event.widget) == tk.Label:

            return

        deltax = self.winfo_width() // 2 - self.center[0]
        deltay = self.winfo_height() // 2 - self.center[1]
        self.center = [self.winfo_width() // 2, self.winfo_height() // 2]

        self.logocanvas.move(self.logo_on_canvas, deltax, deltay)

        if self.tablevar.get() == True:

            fontsize = int(
                round(
                    9.333
                    + 6.6667
                    * (self.parent.winfo_width() / self.parent.winfo_screenwidth()),
                    0,
                )
            )
            if fontsize != self.fontsize:
                for label in self.table.winfo_children():
                    self.fontsize = fontsize
                    if isinstance(label, tk.Label):
                        label.configure(
                            text=label.cget("text"), font=("DejaVu Sans", fontsize)
                        )

        if len(self.rename_boxes) > 0:

            if time.time() > self.starttime:
                try:
                    image_width = self.winfo_width()
                    image_height = self.winfo_height()
                    photoimage_width = self.photoimage.width()
                    photoimage_height = self.photoimage.height()
                    width_factor = image_width / photoimage_width
                    height_factor = image_height / photoimage_height

                    if width_factor <= height_factor:
                        scale_factor = width_factor
                    else:
                        scale_factor = height_factor

                    self.resizable_image = ImageTk.getimage(self.photoimage)
                    self.resized_image = self.resizable_image.resize(
                        (
                            int(self.photoimage.width() * scale_factor),
                            int(self.photoimage.height() * scale_factor),
                        ),
                        Image.ANTIALIAS,
                    )
                    self.canvas.pack_forget()
                    newimage = ImageTk.PhotoImage(self.resized_image)
                    self.canvas.image = newimage
                    self.canvas.itemconfig(
                        self.image_on_canvas, image=self.canvas.image
                    )
                    self.canvas.pack(side=tk.TOP, fill="both", expand=True)
                except AttributeError:
                    pass

            coords = self.canvas.coords(self.image_on_canvas)
            imdims = [self.canvas.image.width(), self.canvas.image.height()]
            canvdims = [self.canvas.winfo_width(), self.canvas.winfo_height()]

            temp = self.rename_boxes[: len(self.DoseFigureHandler.plots)]
            if len(self.rename_boxes) == 1:
                temp = self.rename_boxes

            self.canvas.delete("rename")
            self.rename_boxes = []
            for i in range(len(temp)):
                normdiff = 0
                factor = 1
                if self.norm.get() == False:
                    normdiff = -0.025
                if self.DoseFigureHandler.plots[0].direction == "Z":
                    factor = 6 / 5

                self.rename_boxes += [
                    self.canvas.create_rectangle(
                        coords[0]
                        + imdims[0]
                        * (
                            0.44
                            - 0.0085
                            * max(
                                map(
                                    len,
                                    [
                                        plot.filename
                                        for plot in self.DoseFigureHandler.plots
                                    ],
                                )
                            )
                        ),
                        (coords[1] - imdims[1] * (0.478 - i * 0.035 + normdiff))
                        * factor,
                        coords[0] + imdims[0] * 0.49,
                        (coords[1] - imdims[1] * (0.443 - i * 0.035 + normdiff))
                        * factor,
                        fill="",
                        outline="",
                        tags="rename",
                    )
                ]

            self.canvas.delete("token")

            if self.zoom.get() == True:
                self.oval = self.canvas.create_oval(
                    self.pixelx * (self.canvas.image.width())
                    - 5
                    + (canvdims[0] - imdims[0]) // 2,
                    self.pixely * (self.canvas.image.height())
                    + (canvdims[1] - imdims[1]) // 2
                    - 5,
                    self.pixelx * (self.canvas.image.width())
                    + 5
                    + (canvdims[0] - imdims[0]) // 2,
                    self.pixely * (self.canvas.image.height())
                    + 5
                    + (canvdims[1] - imdims[1]) // 2,
                    fill="",
                    outline="",
                    tags="token",
                )

            self.canvas.delete("xaxis")
            if len(self.DoseFigureHandler.plots) >= 1:
                coords = self.canvas.coords(self.image_on_canvas)
                xbox = self.canvas.create_rectangle(
                    coords[0] - imdims[0] * (0.035 + normdiff / 4),
                    imdims[1] * 0.95 + (canvdims[1] - imdims[1]) // 2,
                    coords[0] + imdims[0] * (0.065 - normdiff / 4),
                    imdims[1] + (canvdims[1] - imdims[1]) // 2,
                    tags="xaxis",
                    outline="",
                    fill="",
                )
                self.rename_boxes += [xbox]

            self.canvas.move(self.image_on_canvas, deltax, deltay)

        self.starttime = time.time()
        try:
            if (
                width_factor != 1
                and newimage.width() == photoimage_width
                and photoimage_width > 0
            ) or (
                height_factor != 1
                and photoimage_height > 0
                and newimage.height() == photoimage_height
            ):
                self.after(10, lambda: self.handle_configure(event))
        except UnboundLocalError:
            pass

    def check_hand(self, e):

        """Shows a different curson when hovering over a rename box
        """

        if e != None:
            try:
                hoverlist = []
                for box in self.rename_boxes:
                    bbox = self.canvas.bbox(box)
                    if (
                        bbox[0] < e.x
                        and bbox[2] > e.x
                        and bbox[1] < e.y
                        and bbox[3] > e.y
                    ):
                        hoverlist += [True]
                    else:
                        hoverlist += [False]
            except TypeError:
                self.show_preview()

            if True in hoverlist:
                self.canvas.config(cursor="hand1")
            else:
                self.canvas.config(cursor="")

            try:
                self.index = hoverlist.index(True)
            except Exception as e:
                self.index = None

    def check_click(self, e):

        """Renames a plot when the associated box is clicked
        """

        for index, box in enumerate(self.rename_boxes):
            if e != None:
                bbox = self.canvas.bbox(box)
                if bbox != None:
                    if (
                        bbox[0] < e.x
                        and bbox[2] > e.x
                        and bbox[1] < e.y
                        and bbox[3] > e.y
                    ):
                        if index == len(self.rename_boxes) - 1:
                            if self.xlimmenu == False:
                                self.change_xrange()
                            else:
                                newname = sd.askstring(
                                    "",
                                    self.text.changefilename[self.lang],
                                    initialvalue=self.DoseFigureHandler.xlabel,
                                )
                                if newname != None:
                                    self.DoseFigureHandler.xaxisname = newname
                                    self.show_preview()
                            return
                        newname = sd.askstring(
                            "",
                            self.text.changefilename[self.lang],
                            initialvalue=self.DoseFigureHandler.plots[index].filename,
                        )
                        if newname != None:
                            self.DoseFigureHandler.plots[index].filename = newname
                            self.show_preview()

    def check_right_click(self, e):

        """Reassigns a color to a plot when the associated box is right-clicked
        """

        for index, box in enumerate(self.rename_boxes[:-1]):
            if e != None:
                bbox = self.canvas.bbox(box)
                if bbox != None:
                    if (
                        bbox[0] < e.x
                        and bbox[2] > e.x
                        and bbox[1] < e.y
                        and bbox[3] > e.y
                    ):
                        newcolor = askcolor(color=self.DoseFigureHandler.colors[index])
                        if newcolor != (None, None):
                            self.DoseFigureHandler.colors[index] = newcolor[1]
                            self.profile.set_attribute(
                                "colors", self.DoseFigureHandler.colors
                            )
                            self.show_preview()

