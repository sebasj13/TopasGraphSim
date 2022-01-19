import os
import tkinter as tk
from tkinter import filedialog as fd

from PIL import Image, ImageTk

from .dose_figure_handler import DoseFigureHandler


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.parent.bind("<Control-d>", self.d_key)
        self.parent.bind("<Control-o>", self.o_key)
        self.parent.bind("<Control-s>", self.s_key)
        self.parent.bind("<Control-t>", self.t_key)
        self.parent.bind("<Escape>", self.esc_key)
        self.parent.bind("<Control-z>", self.z_key)

        self.pack(side="top", fill="both", expand=True)

        self.menubar = tk.Menu(self.parent)

        self.filemenu = tk.Menu(self.menubar, tearoff=False)

        self.addmeasuremenu = tk.Menu(self.menubar, tearoff=False)

        self.addmeasuremenu.add_command(
            label="Tiefendosiskurve",
            command=lambda: self.load_file("pdd"),
            accelerator="Ctrl+T",
        )
        self.addmeasuremenu.add_command(
            label="Dosisquerverteilung",
            command=lambda: self.load_file("dp"),
            accelerator="Ctrl+D",
        )

        self.filemenu.add_command(
            label="Simulationsergebnis laden",
            command=lambda: self.load_file("simulation"),
            accelerator="Ctrl+O",
        )
        self.filemenu.add_cascade(label="Messung laden", menu=self.addmeasuremenu)
        self.filemenu.add_separator()
        self.filemenu.add_command(
            label="Ergebnis abspeichern", command=self.save_graph, accelerator="Ctrl+S"
        )
        self.filemenu.add_command(
            label="Derzeitige Simulation schließen",
            command=self.close_file,
            accelerator="Esc",
        )
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Beenden", command=self.parent.destroy)

        self.filemenu.entryconfig(3, state=tk.DISABLED)
        self.filemenu.entryconfig(4, state=tk.DISABLED)

        self.addmenu = tk.Menu(self.menubar, tearoff=False)

        self.addmenu.add_command(
            label="Simulationsergebnis",
            command=lambda: self.load_file("simulation"),
            accelerator="Ctrl+O",
        )
        self.addmenu.add_cascade(label="Messung", menu=self.addmeasuremenu)
        self.addmenu.add_separator()
        self.addmenu.add_command(
            label="Rückgängig", command=self.remove_last_addition, accelerator="Ctrl+Z"
        )
        self.addmenu.entryconfig(3, state=tk.DISABLED)

        self.menubar.add_cascade(label="Datei", menu=self.filemenu)
        self.menuflag = False
        self.parent.config(menu=self.menubar)

        self.DoseFigureHandler = DoseFigureHandler()

        self.canvas = tk.Canvas(self)
        self.photoimage = None
        self.image_on_canvas = None
        self.canvas.image = None

        self.current_file = None
        self.filenames = []

    def load_file(self, type):

        if type == "simulation":
            filetypes = [("Simulationsergebnisse", ".csv")]
        else:
            filetypes = [("Messdaten", ["txt", ".csv"])]

        self.current_file = fd.askopenfilename(
            title="Datei auswählen...", initialdir=os.getcwd(), filetypes=filetypes
        )

        if self.current_file == "":
            return

        self.filenames += [(self.current_file, type)]

        self.show_preview()
        self.filemenu.entryconfig(0, state=tk.DISABLED)
        self.filemenu.entryconfig(1, state=tk.DISABLED)
        self.filemenu.entryconfig(3, state=tk.NORMAL)
        self.filemenu.entryconfig(4, state=tk.NORMAL)

    def d_key(self, event=None):
        self.load_file("dp")

    def o_key(self, event=None):
        self.load_file("simulation")

    def t_key(self, event=None):
        self.load_file("pdd")

    def close_file(self):

        self.canvas.pack_forget()
        self.filemenu.entryconfig(0, state=tk.NORMAL)
        self.filemenu.entryconfig(1, state=tk.NORMAL)
        self.filemenu.entryconfig(3, state=tk.DISABLED)
        self.filemenu.entryconfig(4, state=tk.DISABLED)
        self.menubar.delete(1)
        self.filenames = []
        self.canvas.itemconfig(self.image_on_canvas, image=None)
        self.menuflag = False
        self.DoseFigureHandler.flush()

    def esc_key(self, event=None):
        self.close_file()

    def remove_last_addition(self):

        self.filenames.pop(-1)
        if len(self.filenames) < 2:
            self.addmenu.entryconfig(3, state=tk.DISABLED)

        if len(self.filenames) <= 4:
            self.addmenu.entryconfig(0, state=tk.NORMAL)
            self.addmenu.entryconfig(1, state=tk.NORMAL)

        self.canvas.itemconfig(self.image_on_canvas, image=None)
        self.DoseFigureHandler.flush()
        self.show_preview()

    def z_key(self, event=None):
        self.remove_last_addition()

    def save_graph(self):

        file = fd.asksaveasfilename(
            defaultextension=".png", filetypes=[("Bilder", [".png", ".jpg"])]
        )

        if file is None:
            return

        ImageTk.getimage(self.photoimage).save(file)
        return

    def s_key(self, event=None):
        self.save_graph()

    def show_preview(self):

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
            self.menubar.add_cascade(label="Hinzufügen...", menu=self.addmenu)
            self.menuflag = True
        self.image_on_canvas = self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.photoimage
        )

        self.canvas.image = self.photoimage
        self.canvas.itemconfig(self.image_on_canvas, image=self.canvas.image)

    def handle_configure(self, event):

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
