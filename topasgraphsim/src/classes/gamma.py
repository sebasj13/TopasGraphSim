import tkinter as tk
import tkinter.ttk as ttk

from ..resources.language import Text


class ChangeGamma:
    def __init__(self, parent) -> None:

        self.parent = parent
        self.gammathreshold = self.parent.gammathreshold
        self.gammadist = self.parent.gammadist

        self.top = tk.Toplevel()
        self.geometry = [
            self.parent.parent.winfo_rootx(),
            self.parent.parent.winfo_rooty(),
            self.parent.winfo_width(),
            self.parent.winfo_height(),
        ]
        self.width = 110
        self.height = 140

        self.top.geometry(
            f"{self.width}x{self.height}+{self.parent.winfo_rootx()}+{self.parent.parent.winfo_rooty()}"
        )
        self.top.overrideredirect(1)

        self.top.bind("<Return>", self.submit)
        self.top.bind("<Escape>", self.top.destroy)
        self.enterlabel = ttk.Label(self.top, text="Gamma-Index")
        self.enterbox1 = ttk.Entry(self.top, width=3)
        self.enterbox1.insert(tk.END, self.gammathreshold)
        self.percentlabel = ttk.Label(self.top, text="%")
        self.enterbox2 = ttk.Entry(self.top, width=3)
        self.enterbox2.insert(tk.END, self.gammadist)
        self.mmtabel = ttk.Label(self.top, text="mm")

        self.enterlabel.grid(row=0, column=0, columnspan=2, padx=(5, 5), pady=(2, 2))
        self.enterbox1.grid(row=1, column=0, padx=(1, 1), pady=(2, 2))
        self.percentlabel.grid(row=1, column=1, padx=(1, 1), pady=(2, 2))
        self.enterbox2.grid(row=2, column=0, padx=(1, 1), pady=(2, 2))
        self.mmtabel.grid(row=2, column=1, padx=(1, 1), pady=(2, 2))
        self.submitbutton = ttk.Button(
            self.top, text=Text().submit[self.parent.lang], command=self.submit,
        )
        self.submitbutton.grid(row=3, column=0, columnspan=2, padx=(5, 5), pady=(2, 2))

        self.enterbox1.focus()
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

        try:
            self.gammathreshold = float(self.enterbox1.get())
            self.gammadist = float(self.enterbox2.get())
        except Exception:
            self.top.destroy()

        if self.gammadist > 0 and self.gammathreshold > 0:

            self.parent.gammathreshold = self.gammathreshold
            self.parent.gammadist = self.gammadist
            self.parent.gammaacc.set(f"{self.gammathreshold}%/{self.gammadist}mm")
            self.parent.gammamenu.entryconfig(1, accelerator=self.parent.gammaacc.get())

        self.top.destroy()
