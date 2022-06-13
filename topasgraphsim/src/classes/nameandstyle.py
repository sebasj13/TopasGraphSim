import tkinter as tk
import tkinter.ttk as ttk

from ..resources.language import Text


class GraphNameAndStyle:
    def __init__(self, parent, index) -> None:

        self.parent = parent
        self.index = index

        self.top = tk.Toplevel()
        try:
            if self.index >= len(self.parent.DoseFigureHandler.plots):
                self.top.destroy()
        except TypeError:
            pass
        self.geometry = [
            self.parent.parent.winfo_rootx(),
            self.parent.parent.winfo_rooty(),
            self.parent.winfo_width(),
            self.parent.winfo_height(),
        ]
        self.width = 225
        self.height = 110
        if self.index == "X":
            self.width = 130

        self.top.geometry(
            f"{self.width}x{self.height}+{self.parent.winfo_rootx()}+{self.parent.parent.winfo_rooty()}"
        )
        self.top.overrideredirect(1)

        self.top.bind("<Return>", self.submit)
        self.top.bind("<Escape>", self.top.destroy)
        self.enterlabel = ttk.Label(
            self.top, text=Text().changefilename[self.parent.lang]
        )
        self.enterbox = ttk.Entry(self.top, width=15)

        self.enterlabel.grid(row=0, column=0, padx=(5, 5), pady=(2, 2))
        self.enterbox.grid(row=1, column=0, padx=(5, 5), pady=(2, 2))
        self.submitbutton = ttk.Button(
            self.top, text=Text().submit[self.parent.lang], command=self.submit,
        )
        self.submitbutton.grid(row=2, column=0, padx=(5, 5), pady=(2, 2))

        if index != "X":
            self.enterbox.insert(
                tk.END, string=self.parent.DoseFigureHandler.plots[index].filename
            )
            self.radiovar = tk.StringVar()
            self.radiovar.set(self.parent.DoseFigureHandler.marker[index])
            self.values = [".", "-", "o--"]
            self.styles = [
                Text().dot[self.parent.lang],
                Text().dash[self.parent.lang],
                Text().dashdot[self.parent.lang],
            ]
            self.radiobuttons = [
                ttk.Radiobutton(
                    self.top,
                    variable=self.radiovar,
                    value=self.values[i],
                    text=self.styles[i],
                )
                for i in range(3)
            ]

            for i, button in enumerate(self.radiobuttons):
                button.grid(row=i, column=1, padx=(0, 5), sticky=tk.W, pady=(2, 2))
        else:
            xlabel = self.parent.DoseFigureHandler.xaxisname
            if xlabel == None:
                xlabel = self.parent.DoseFigureHandler.xlabel
            self.enterbox.insert(tk.END, string=xlabel)

        self.enterbox.focus()
        self.lift()

    def lift(self):
        self.new_geometry = [
            self.parent.parent.winfo_rootx(),
            self.parent.parent.winfo_rooty(),
            self.parent.winfo_width(),
            self.parent.winfo_height(),
        ]

        self.top.lift()
        self.top.after(100, self.lift)
        if self.new_geometry == self.geometry:
            return

        self.geometry = self.new_geometry
        self.top.geometry(
            f"{self.width}x{self.height}+{self.parent.winfo_rootx()}+{self.parent.parent.winfo_rooty()}"
        )

    def submit(self, event=None):

        self.top.unbind("<Return>")

        if self.index == "X":
            self.parent.DoseFigureHandler.xaxisname = self.enterbox.get()

        else:
            self.parent.DoseFigureHandler.plots[
                self.index
            ].filename = self.enterbox.get()
            self.parent.DoseFigureHandler.marker[self.index] = self.radiovar.get()
            self.parent.profile.set_attribute(
                "markers", self.parent.DoseFigureHandler.marker
            )

        self.top.destroy()
