import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd

from PIL import Image, ImageTk

from ..resources.language import Text
from .dose_figure_handler import DoseFigureHandler
from .profile import ProfileHandler


class MainApplication(tk.Frame):
    def __init__(self, parent, geometry, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        # Read settings from profile.json and initialize the necessary variables
        self.profile = ProfileHandler()
        self.lang = self.profile.get_attribute("language")
        self.langvar = tk.StringVar()
        self.langvar.set(self.lang)
        self.text = Text()
        self.dark = tk.BooleanVar()
        self.dark.set(False)
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
        color_scheme = self.profile.get_attribute("color_scheme")
        self.autostartdark = tk.StringVar()
        self.autostartdark.set(color_scheme)
        self.autostart()

        # Keybinding definitions
        self.parent.bind("<Control-d>", self.d_key)
        self.parent.bind("<Control-o>", self.o_key)
        self.parent.bind("<Control-s>", self.s_key)
        self.parent.bind("<Control-t>", self.t_key)
        self.parent.bind("<Escape>", self.esc_key)
        self.parent.bind("<Control-z>", self.z_key)

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
            label=self.text.end[self.lang], command=self.parent.destroy
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
        self.parent.config(menu=self.menubar)

        # Initialize necessary variables
        self.menuflag = False
        self.canvas = tk.Canvas(self)
        self.photoimage = None
        self.image_on_canvas = None
        self.canvas.image = None
        self.current_file = None
        self.filenames = []

        self.parent.geometry(geometry)
        self.pack(side="top", fill="both", expand=True)

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
            self.DoseFigureHandler.set_style()
            self.dark.set(False)

        else:
            # Set dark theme
            self.parent.tk.call("set_theme", "dark")
            self.DoseFigureHandler.set_style()
            self.parent.configure(background="#363636")
            self.dark.set(True)

    def set_language(self, language):

        """
        Sets the desired language and reinitiates the program
        """

        geometry = self.parent.winfo_geometry()

        if self.menuflag == True:
            warning = tk.messagebox.askokcancel(
                message=self.text.languageset[self.lang]
            )

            if warning == True:
                self.pack_forget()
                self.parent.config(menu=None)
                self.profile.set_attribute("language", language)
                self.__init__(self.parent, geometry)
            return
        self.pack_forget()
        self.parent.config(menu=None)
        self.profile.set_attribute("language", language)
        self.__init__(self.parent, geometry)
        return

    def load_file(self, type):

        """
        Loads measurement or simulation data to be displayed
        """

        if type == "simulation":
            filetypes = [("Simulationsergebnisse", ".csv")]
        else:
            filetypes = [("Messdaten", ["txt", ".csv"])]

        self.current_file = fd.askopenfilename(
            initialdir=os.getcwd(), filetypes=filetypes
        )

        if self.current_file == "":
            return

        self.filenames += [(self.current_file, type)]

        self.show_preview()
        self.filemenu.entryconfig(0, state=tk.DISABLED)
        self.filemenu.entryconfig(1, state=tk.DISABLED)
        self.filemenu.entryconfig(3, state=tk.NORMAL)
        self.filemenu.entryconfig(4, state=tk.NORMAL)

    def close_file(self):

        """
        Closes the current project
        """

        self.canvas.pack_forget()
        self.filemenu.entryconfig(0, state=tk.NORMAL)
        self.filemenu.entryconfig(1, state=tk.NORMAL)
        self.filemenu.entryconfig(3, state=tk.DISABLED)
        self.filemenu.entryconfig(4, state=tk.DISABLED)
        self.menubar.delete(3)
        self.filenames = []
        self.canvas.itemconfig(self.image_on_canvas, image=None)
        self.menuflag = False
        self.DoseFigureHandler.flush()

    def remove_last_addition(self):

        """
        Removes the graph added last
        """

        self.filenames.pop(-1)
        if len(self.filenames) < 2:
            self.addmenu.entryconfig(3, state=tk.DISABLED)

        if len(self.filenames) <= 4:
            self.addmenu.entryconfig(0, state=tk.NORMAL)
            self.addmenu.entryconfig(1, state=tk.NORMAL)

        self.canvas.itemconfig(self.image_on_canvas, image=None)
        self.DoseFigureHandler.flush()
        self.show_preview()

    def save_graph(self):

        """
        Saves the current graph
        """

        file = fd.asksaveasfilename(
            defaultextension=".png", filetypes=[("Bilder", [".png", ".jpg"])]
        )

        if file is None:
            return

        ImageTk.getimage(self.photoimage).save(file)
        return

    def show_preview(self):

        """
        Invokes DoseFigureHandler to create and display the graphs
        """

        self.photoimage, menuflag = self.DoseFigureHandler.return_figure(self.filenames)

        self.canvas.pack_forget()
        self.canvas = tk.Canvas(self)
        self.canvas.bind("<Configure>", self.handle_configure)
        self.canvas.pack(fill="both", expand=True)

        if len(self.filenames) >= 2:
            self.addmenu.entryconfig(3, state=tk.NORMAL)

        if len(self.filenames) == 5:
            self.addmenu.entryconfig(0, state=tk.DISABLED)
            self.addmenu.entryconfig(1, state=tk.DISABLED)

        if menuflag == "Z" and self.menuflag == False:
            self.menubar.add_cascade(label=self.text.add[self.lang], menu=self.addmenu)
            self.menuflag = True
        self.image_on_canvas = self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.photoimage
        )

        self.canvas.image = self.photoimage
        self.canvas.itemconfig(self.image_on_canvas, image=self.canvas.image)

    def handle_configure(self, event):

        """
        Dynamically resizes the graph according to the window size
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

    # Keybing functions
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

    def s_key(self, event=None):
        self.save_graph()
