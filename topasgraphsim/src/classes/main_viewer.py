import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
from tkinter.colorchooser import askcolor

import win32api
from PIL import Image, ImageTk

from ..resources.language import Text
from .dose_figure_handler import DoseFigureHandler
from .profile import ProfileHandler


class MainApplication(tk.Frame):
    def __init__(self, parent):

        tk.Frame.__init__(self, parent)

        self.parent = parent

        self.parent.protocol("WM_DELETE_WINDOW", lambda: self.save_graph(True))

        # Read settings from profile.json and initialize the necessary variables

        self.saved = True
        self.menuflag = False
        self.canvas = tk.Canvas(self)
        self.photoimage = None
        self.image_on_canvas = None
        self.canvas.image = None
        self.current_file = None
        self.filenames = []
        self.rename_boxes = []

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

        self.zoom = tk.BooleanVar()
        self.zoom.set(bool(self.profile.get_attribute("zoom")))

        self.half = tk.BooleanVar()
        self.half.set(bool(self.profile.get_attribute("halfview")))

        self.calcparams = tk.BooleanVar()
        self.calcparams.set(False)

        self.fullscreen = tk.BooleanVar()
        self.fullscreen.set(bool(self.profile.get_attribute("fullscreen")))

        self.axlims = tk.IntVar()
        self.axlims.set(0)

        self.normvaluemenu = tk.StringVar()
        self.normvaluemenu.set("max")

        self.DoseFigureHandler = DoseFigureHandler(self)

        # Keybinding definitions
        self.parent.bind("<Control-d>", lambda type: self.load_file("dp"))
        self.parent.bind("<Control-o>", lambda type: self.load_file("simulation"))
        self.parent.bind("<Control-s>", self.save_graph)
        self.parent.bind("<Control-t>", lambda type: self.load_file("pdd"))
        self.parent.bind("<Control-p>", lambda type: self.load_file("ptw"))
        self.parent.bind("<Escape>", self.close_file)
        self.parent.bind("<Control-z>", self.remove_last_addition)
        self.parent.bind("<F11>", self.toggle_fullscreen)
        self.parent.bind("<MouseWheel>", self.change_x_limits)
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
            label="3Ddose", command=lambda: self.load_file("egs"),
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
        self.normmenu.add_checkbutton(
            label=self.text.calcparams[self.lang],
            command=self.calculate_parameters,
            variable=self.calcparams,
        )

        self.normmenu.add_checkbutton(
            label=self.text.caxcorrection[self.lang],
            command=self.correct_caxdev,
            variable=self.caxcorrection,
        )

        self.normmenu.entryconfig(10, state=tk.DISABLED)
        self.parent.config(menu=self.menubar)

        self.parent.title(self.text.window_title[self.lang])
        self.pack(side="top", fill="both", expand=True)
        self.parent.attributes("-fullscreen", self.fullscreen.get())
        self.autostart()

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
            self.parent.configure(background="#ffffff")
            if self.filenames != []:
                self.show_preview()

        else:
            # Set dark theme
            self.parent.tk.call("set_theme", "dark")
            self.parent.configure(background="#363636")
            if self.filenames != []:
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
            self.axlims.set(self.axlims.get() - 5)
        elif event.delta < 0:
            self.axlims.set(self.axlims.get() + 5)
        self.show_preview()

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
        self.pack_forget()
        self.parent.config(menu=None)
        self.profile.set_attribute("language", language)
        self.__init__(self.parent)
        if plots != []:
            self.filenames = filenames
            self.DoseFigureHandler.plots = plots
            self.dark.set(dark)
            self.axlims.set(axlims)
            self.calcparams.set(calcparams)
            self.caxcorrection.set(caxcorrection)
            self.norm.set(normalize)
            self.errorbars.set(errorbars)
            self.show_preview()

        return

    def load_file(self, type, event=None):

        """Loads measurement or simulation data to be displayed
        """

        if type == "simulation":
            filetypes = [(self.text.topas[self.lang], [".csv", ".bin"])]
        if type == "egs":
            filetypes = [(self.text.egs[self.lang], [".csv", ".bin"])]
        elif type == "pdd" or type == "dp":
            filetypes = [(self.text.measurementdata[self.lang], ["txt", ".csv"])]
        elif type == "ptw":
            filetypes = [(self.text.ptw[self.lang], ".mcc")]
        self.current_file = fd.askopenfilenames(
            initialdir=os.getcwd(), filetypes=filetypes
        )

        if self.current_file == "":
            return

        for file in self.current_file:
            self.filenames += [(file, type)]

        self.show_preview()
        self.filemenu.entryconfig(0, state=tk.DISABLED)
        self.filemenu.entryconfig(1, state=tk.DISABLED)
        self.filemenu.entryconfig(3, state=tk.NORMAL)
        self.filemenu.entryconfig(4, state=tk.NORMAL)
        self.saved = False

        return

    def close_file(self, event=None):

        """Closes the current project
        """

        self.canvas.place_forget()
        self.filemenu.entryconfig(0, state=tk.NORMAL)
        self.filemenu.entryconfig(1, state=tk.NORMAL)
        self.filemenu.entryconfig(3, state=tk.DISABLED)
        self.filemenu.entryconfig(4, state=tk.DISABLED)
        self.addmenu.entryconfig(0, state=tk.NORMAL)
        self.addmenu.entryconfig(1, state=tk.NORMAL)
        self.addmeasuremenu.entryconfig(0, state=tk.NORMAL)
        self.addmeasuremenu.entryconfig(1, state=tk.NORMAL)
        self.menubar.delete(3, 4)
        self.filenames = []
        self.canvas.itemconfig(self.image_on_canvas, image=None)
        self.DoseFigureHandler.flush()
        self.DoseFigureHandler.plots = []
        self.saved = True
        self.menuflag = False
        self.DoseFigureHandler.caxcorrection = False
        self.caxcorrection.set(False)
        self.axlims.set(0)

        return

    def save_graph(self, exit=False):

        """Saves the current graph as an image
        """

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
            filetypes=[(self.text.image[self.lang], [".png", ".jpg"])],
        )

        if file is None:
            return

        ImageTk.getimage(self.photoimage).save(file)
        self.saved = True

        return

    def normalize(self):

        """Choose whether or not the displayed graph should be normalized
        """

        self.DoseFigureHandler.norm = self.norm.get()

        self.profile.set_attribute("normalize", int(self.norm.get()))
        if self.filenames != []:
            self.canvas.itemconfig(self.image_on_canvas, image=None)
            self.DoseFigureHandler.flush()
            self.show_preview()

        return

    def show_errorbars(self):

        """Choose whether or not the displayed graph should be contain errorbars
        """

        self.DoseFigureHandler.errorbars = self.errorbars.get()

        if self.filenames != []:
            self.canvas.itemconfig(self.image_on_canvas, image=None)
            self.DoseFigureHandler.flush()
            self.show_preview()

        return

    def correct_caxdev(self):

        """Choose whether or not the displayed dose
        profiles should be center-axis-corrected
        """

        self.DoseFigureHandler.caxcorrection = self.caxcorrection.get()

        if self.filenames != []:
            self.canvas.itemconfig(self.image_on_canvas, image=None)
            self.DoseFigureHandler.flush()
            self.show_preview()

        return

    def calculate_parameters(self):

        """Choose whether or not the displayed dose
        profiles should be center-axis-corrected
        """

        self.DoseFigureHandler.calcparams = self.calcparams.get()

        if self.calcparams.get() == True:
            if self.direction != "Z":
                self.normmenu.entryconfig(10, state=tk.NORMAL)
        else:
            self.normmenu.entryconfig(10, state=tk.DISABLED)
            self.caxcorrection.set(False)

        if self.filenames != []:
            self.canvas.itemconfig(self.image_on_canvas, image=None)
            self.DoseFigureHandler.flush()
            self.show_preview()

        return

    def remove_last_addition(self, event=None):

        """
        Removes the graph added last
        """

        if len(self.filenames) == 1:
            self.close_file()
            return

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

        self.DoseFigureHandler.flush()
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

        if self.filenames != []:
            self.canvas.itemconfig(self.image_on_canvas, image=None)
            self.DoseFigureHandler.flush()
            self.show_preview()

        return

    def zoomgraph(self):

        """Choose whether or not the displayed graph
        should contain inset axis for a zoom view
        """

        self.DoseFigureHandler.zoom = self.zoom.get()

        self.profile.set_attribute("zoom", int(self.zoom.get()))

        if self.filenames != []:
            self.canvas.itemconfig(self.image_on_canvas, image=None)
            self.DoseFigureHandler.flush()
            self.show_preview()

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

        if self.filenames != []:
            self.canvas.itemconfig(self.image_on_canvas, image=None)
            self.DoseFigureHandler.flush()
            self.show_preview()

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

        if self.filenames != []:
            self.canvas.itemconfig(self.image_on_canvas, image=None)
            self.DoseFigureHandler.flush()
            self.show_preview()
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
        self.DoseFigureHandler.flush()
        self.photoimage, self.direction = self.DoseFigureHandler.return_figure(
            self.filenames
        )

        self.canvas.place_forget()
        self.canvas = tk.Canvas(self)
        self.canvas.bind("<Configure>", self.handle_configure)
        self.canvas.bind("<Button-1>", self.check_click)
        self.canvas.bind("<Button-3>", self.check_right_click)
        self.canvas.bind("<Motion>", self.check_hand)
        self.canvas.bind("<Double-Button-1>", self.new_zoom)
        self.parent.bind("<Up>", lambda boolean: self.change_order(True))
        self.parent.bind("<Down>", lambda boolean: self.change_order(False))
        self.canvas.place(relheight=1, relwidth=1, relx=0.5, rely=0.5, anchor=tk.CENTER)

        if len(self.DoseFigureHandler.plots) >= 2:
            self.addmenu.entryconfig(3, state=tk.NORMAL)

        if len(self.DoseFigureHandler.plots) == 5:
            self.addmenu.entryconfig(0, state=tk.DISABLED)
            self.addmenu.entryconfig(1, state=tk.DISABLED)
        if self.direction == "Z":
            self.addmeasuremenu.entryconfig(1, state=tk.DISABLED)
            self.normmenu.entryconfig(7, state=tk.DISABLED)
        else:
            self.addmeasuremenu.entryconfig(0, state=tk.DISABLED)
            self.normmenu.entryconfig(7, state=tk.NORMAL)
            self.canvas.place_forget()
            self.canvas.place(
                relheight=1, relwidth=1, relx=0.55556, rely=0.5, anchor=tk.CENTER
            )
        if self.menuflag == False:
            self.menubar.add_cascade(label=self.text.add[self.lang], menu=self.addmenu)
            self.menubar.add_cascade(label="Graph", menu=self.normmenu)
            self.menuflag = True
        self.image_on_canvas = self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.photoimage
        )

        self.canvas.image = self.photoimage
        self.canvas.itemconfig(self.image_on_canvas, image=self.canvas.image)

        for i in range(len(self.DoseFigureHandler.plots)):
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
                (0.023 + 0.042 * i) * self.canvas.image.height() * factor,
                0.988 * self.canvas.image.width(),
                (0.065 + 0.042 * i) * self.canvas.image.height() * factor,
                fill="",
                outline="",
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

            if boolean == True:

                new_index = self.index - 1
                dy = -0.044

                if self.index == 0:
                    new_index = len(self.rename_boxes) - 1
                    dy = 0.044 * (len(self.rename_boxes) - 1)

            else:
                if self.index + 1 == len(self.rename_boxes):
                    new_index = 0
                    dy = -0.044 * (len(self.rename_boxes) - 1)

                else:
                    new_index = self.index + 1
                    dy = 0.044
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
            win32api.SetCursorPos((x, int(y)))
            self.index = new_index
            self.show_preview()
            self.canvas.config(cursor="hand1")
            return

    def handle_configure(self, event):

        """
        Dynamically resizes the graph, rename boxes and zoom window selector
        according to the window size and name length
        """

        try:
            image_width = event.width
            image_height = event.height
            width_factor = image_width / self.photoimage.width()
            height_factor = image_height / self.photoimage.height()

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
            self.canvas.image = ImageTk.PhotoImage(self.resized_image)
            self.canvas.itemconfig(self.image_on_canvas, image=self.canvas.image)
        except AttributeError:
            pass

        temp = self.rename_boxes
        self.rename_boxes = []
        for i in range(len(self.DoseFigureHandler.plots)):
            x = self.canvas.image.width()
            y = self.canvas.image.height()
            self.canvas.delete(temp[i])
            factor = (self.canvas.image.width() / self.canvas.image.height()) / 2
            self.rename_boxes += [
                self.canvas.create_rectangle(
                    (
                        -0.00833
                        * max(
                            map(
                                len,
                                [
                                    plot.filename
                                    for plot in self.DoseFigureHandler.plots
                                ],
                            )
                        )
                        + 0.94633
                    )
                    * x,
                    (0.023 + 0.042 * i) * y * factor,
                    0.988 * x,
                    (0.065 + 0.042 * i) * y * factor,
                    fill="",
                    outline="",
                    tags="rename",
                )
            ]

        self.canvas.delete("token")

        if self.zoom.get() == True:
            self.oval = self.canvas.create_oval(
                self.pixelx * self.canvas.image.width() - 5,
                self.pixely * self.canvas.image.height() - 5,
                self.pixelx * self.canvas.image.width() + 5,
                self.pixely * self.canvas.image.height() + 5,
                fill="",
                outline="",
                tags="token",
            )

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
                if bbox[0] < e.x and bbox[2] > e.x and bbox[1] < e.y and bbox[3] > e.y:
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
                        newcolor = askcolor(color=self.DoseFigureHandler.colors[index])
                        if newcolor != None:
                            self.DoseFigureHandler.colors[index] = newcolor[1]
                            self.profile.set_attribute(
                                "colors", self.DoseFigureHandler.colors
                            )
                            self.show_preview()

