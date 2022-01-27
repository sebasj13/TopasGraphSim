import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
from tkinter.font import NORMAL

from PIL import Image, ImageTk

from ..resources.language import Text
from .dose_figure_handler import DoseFigureHandler
from .profile import ProfileHandler


class MainApplication(tk.Frame):
    def __init__(self, parent, geometry, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)

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

        self.dark = tk.BooleanVar()
        self.dark.set(False)

        self.norm = tk.BooleanVar()
        self.norm.set(bool(self.profile.get_attribute("normalize")))

        self.zoom = tk.BooleanVar()
        self.zoom.set(bool(self.profile.get_attribute("zoom")))

        self.half = tk.BooleanVar()
        self.half.set(bool(self.profile.get_attribute("halfview")))

        self.fullscreen = tk.BooleanVar()
        self.fullscreen.set(bool(self.profile.get_attribute("fullscreen")))

        self.axlims = tk.IntVar()
        self.axlims.set(0)

        self.DoseFigureHandler = DoseFigureHandler(self)

        self.parent.title(self.text.window_title[self.lang])
        style = ttk.Style(self.parent)
        try:
            self.parent.tk.call(
                "source",
                str(
                    os.path.dirname(os.path.realpath(__file__))
                    + "\\..\\Azure-ttk-theme\\azure.tcl"
                ),
            )
        except tk.TclError:
            pass

        self.parent.geometry(geometry)
        self.parent.attributes("-fullscreen", self.fullscreen.get())
        self.pack(side="top", fill="both", expand=True)

        color_scheme = self.profile.get_attribute("color_scheme")
        self.autostartdark = tk.StringVar()
        self.autostartdark.set(color_scheme)
        self.autostart()

        # Keybinding definitions
        self.parent.bind("<Control-d>", self.d_key)
        self.parent.bind("<Control-o>", self.o_key)
        self.parent.bind("<Control-s>", self.s_key)
        self.parent.bind("<Control-t>", self.t_key)
        self.parent.bind("<Control-p>", self.p_key)
        self.parent.bind("<Escape>", self.esc_key)
        self.parent.bind("<Control-z>", self.z_key)
        self.parent.bind("<F11>", self.toggle_fullscreen)
        self.parent.bind("<MouseWheel>", self.change_x_limits)

        # Menubar definitions
        self.menubar = tk.Menu(self.parent)
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

        self.filemenu.add_command(
            label=self.text.loadsim[self.lang],
            command=lambda: self.load_file("simulation"),
            accelerator="Ctrl+O",
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
        self.addmenu.add_command(
            label=self.text.simulation[self.lang],
            command=lambda: self.load_file("simulation"),
            accelerator="Ctrl+O",
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
        self.optionsmenu = tk.Menu(self.menubar)
        self.optionsmenu.add_checkbutton(
            label=self.text.startdark[self.lang],
            variable=self.autostartdark,
            command=lambda: self.profile.set_attribute(
                "color_scheme", f"{self.autostartdark.get()}"
            ),
            onvalue="dark",
            offvalue="light",
        )
        self.langmenu = tk.Menu(self.menubar)
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

        self.normmenu = tk.Menu(self.menubar)

        self.markersizemenu = tk.Menu(self.menubar)
        self.markersizemenu.add_command(
            label=Text().increase[self.lang],
            command=lambda: self.change_marker_size(True),
            accelerator="Ctrl + ↑",
        )
        self.parent.bind("<Control-Up>", self.up_down_key)
        self.markersizemenu.add_command(
            label=Text().decrease[self.lang],
            command=lambda: self.change_marker_size(False),
            accelerator="Ctrl + ↓",
        )
        self.parent.bind("<Control-Down>", self.up_down_key)

        self.markerlinemenu = tk.Menu(self.menubar)
        self.markerlinemenu.add_command(
            label=Text().increase[self.lang],
            command=lambda: self.change_line_width(True),
            accelerator="Ctrl + →",
        )
        self.parent.bind("<Control-Right>", self.right_left_key)
        self.markerlinemenu.add_command(
            label=Text().decrease[self.lang],
            command=lambda: self.change_line_width(False),
            accelerator="Ctrl + ←",
        )
        self.parent.bind("<Control-Left>", self.right_left_key)

        self.normmenu.add_cascade(
            label=Text().markerline[self.lang], menu=self.markerlinemenu
        )
        self.normmenu.add_cascade(
            label=Text().marker[self.lang], menu=self.markersizemenu
        )

        self.normmenu.add_separator()
        self.normmenu.add_checkbutton(
            label=self.text.normalize[self.lang],
            command=self.normalize,
            variable=self.norm,
        )

        self.normmenu.add_checkbutton(
            label=self.text.zoom[self.lang], command=self.zoomgraph, variable=self.zoom,
        )
        self.normmenu.add_checkbutton(
            label=self.text.half[self.lang], command=self.halfgraph, variable=self.half,
        )

        self.parent.config(menu=self.menubar)

    def toggle_fullscreen(self, event=None):
        self.parent.attributes("-fullscreen", not self.parent.attributes("-fullscreen"))
        self.fullscreen.set(self.parent.attributes("-fullscreen"))
        self.profile.set_attribute("fullscreen", bool(self.fullscreen.get()))

    def autostart(self):

        """
        Sets the theme according to the profile.json
        """

        if self.autostartdark.get() == "light":
            self.dark.set(False)
            self.switchtheme("light")
        else:
            self.dark.set(True)
            self.switchtheme("dark")
        return

    def switchtheme(self, theme):

        """
        Switches between light and dark theme
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

    def change_x_limits(self, event=None):
        if event.delta > 0:
            self.axlims.set(self.axlims.get() - 5)
        elif event.delta < 0:
            self.axlims.set(self.axlims.get() + 5)
        self.show_preview()

    def set_language(self, language):

        """
        Sets the desired language and reinitiates the program
        """

        plots = self.DoseFigureHandler.plots
        axlims = self.axlims.get()
        self.pack_forget()
        geometry = self.parent.winfo_geometry()
        self.parent.config(menu=None)
        self.profile.set_attribute("language", language)
        self.__init__(self.parent, geometry)
        self.DoseFigureHandler.plots = plots
        self.axlims.set(axlims)
        self.show_preview()

        return

    def normalize(self):

        self.DoseFigureHandler.norm = self.norm.get()

        self.profile.set_attribute("normalize", int(self.norm.get()))

        if self.filenames != []:
            self.canvas.itemconfig(self.image_on_canvas, image=None)
            self.DoseFigureHandler.flush()
            self.show_preview()
        return

    def zoomgraph(self):
        self.DoseFigureHandler.zoom = self.zoom.get()

        self.profile.set_attribute("zoom", int(self.zoom.get()))

        if self.filenames != []:
            self.canvas.itemconfig(self.image_on_canvas, image=None)
            self.DoseFigureHandler.flush()
            self.show_preview()
        return

    def halfgraph(self):
        self.DoseFigureHandler.half = self.half.get()
        self.profile.set_attribute("halfview", self.half.get())
        self.show_preview()
        return

    def change_marker_size(self, boolean):
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

    def change_line_width(self, boolean):
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

    def load_file(self, type):

        """
        Loads measurement or simulation data to be displayed
        """

        if type == "simulation":
            filetypes = [(self.text.simulationdata[self.lang], ".csv")]
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

    def close_file(self):

        """
        Closes the current project
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
        self.menubar.delete(3, 4)
        self.filenames = []
        self.canvas.itemconfig(self.image_on_canvas, image=None)
        self.menuflag = False
        self.DoseFigureHandler.flush()
        self.DoseFigureHandler.plots = []
        self.saved = True
        self.axlims.set(0)

    def remove_last_addition(self):

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

    def save_graph(self, exit=False):

        """
        Saves the current graph
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

    def show_preview(self):

        """
        Invokes DoseFigureHandler to create and display the graphs
        """
        self.DoseFigureHandler.flush()
        self.photoimage, menuflag = self.DoseFigureHandler.return_figure(self.filenames)

        self.canvas.pack_forget()
        self.canvas = tk.Canvas(self)
        self.canvas.bind("<Configure>", self.handle_configure)
        self.canvas.bind("<Button-1>", self.check_click)
        self.canvas.bind("<Motion>", self.check_hand)
        self.canvas.bind("<Double-Button-1>", self.new_zoom)
        self.canvas.pack(side=tk.TOP, fill="both", expand=True)

        if len(self.DoseFigureHandler.plots) >= 2:
            self.addmenu.entryconfig(3, state=tk.NORMAL)

        if len(self.DoseFigureHandler.plots) == 5:
            self.addmenu.entryconfig(0, state=tk.DISABLED)
            self.addmenu.entryconfig(1, state=tk.DISABLED)

        if menuflag == "Z":
            self.addmeasuremenu.entryconfig(1, state=tk.DISABLED)
            self.normmenu.entryconfig(5, state=tk.DISABLED)
        else:
            self.addmeasuremenu.entryconfig(0, state=tk.DISABLED)
            self.normmenu.entryconfig(5, state=tk.NORMAL)

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

    def handle_configure(self, event):

        """
        Dynamically resizes the graph and rename boxes according to the window size and name length
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

    def check_click(self, e):
        for index, box in enumerate(self.rename_boxes):
            if e != None:
                bbox = self.canvas.bbox(box)
                if bbox[0] < e.x and bbox[2] > e.x and bbox[1] < e.y and bbox[3] > e.y:
                    newname = sd.askstring("", self.text.changefilename[self.lang],)
                    if newname != None:
                        self.DoseFigureHandler.plots[index].filename = newname
                        self.show_preview()

    def esc_key(self, event=None):
        self.close_file()

    def d_key(self, event=None):
        self.load_file("dp")

    def o_key(self, event=None):
        self.load_file("simulation")

    def t_key(self, event=None):
        self.load_file("pdd")

    def z_key(self, event=None):
        self.remove_last_addition()

    def p_key(self, event=None):
        self.load_file("ptw")

    def s_key(self, event=None):
        self.save_graph()

    def up_down_key(self, event=None):
        if event.keysym == "Up":
            self.change_marker_size(True)
        else:
            self.change_marker_size(False)

    def right_left_key(self, event=None):
        if event.keysym == "Right":
            self.change_line_width(True)
        else:
            self.change_line_width(False)
