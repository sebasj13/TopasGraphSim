import time
import tkinter as tk
import tkinter.ttk as ttk

from ..resources.language import Text
from .profile import ProfileHandler
from .RangeSlider import RangeSliderH


class XRangeSlider:
    def __init__(self, parent, slidervars, initial_limits):

        self.parent = parent
        self.window = tk.Toplevel()
        self.window.resizable(False, False)
        self.window.wm_overrideredirect(True)
        self.window.wm_attributes("-alpha", 0.6)
        self.window.bind("<Return>", self.submit)
        self.dark = self.parent.dark.get()
        self.geometry = [
            self.parent.parent.winfo_rootx(),
            self.parent.parent.winfo_rooty(),
            self.parent.winfo_width(),
            self.parent.winfo_height(),
        ]
        self.height = 110
        self.window.geometry(
            f"{500}x{self.height}+{int(self.geometry[0]+self.geometry[2]//2) - 250}+{int(self.geometry[1]+self.geometry[3]//2)}"
        )

        try:
            self.parent.table.pack_forget()
        except AttributeError:
            pass

        self.parent.tablevar.set(False)

        self.slider = RangeSliderH(
            self.window,
            variables=slidervars,
            padX=100,
            valueSide="BOTTOM",
            Width=500,
            min_val=initial_limits[0],
            max_val=initial_limits[1],
            font_family="Helvetica",
            font_size=12,
            digit_precision=".0f",
            suffix=" mm",
        )
        if self.dark == True:
            self.slider.canv.configure(bg="#363636")
            self.slider.canv.itemconfigure(self.slider.bars[0]["Ids"][2], fill="white")
            self.slider.canv.itemconfigure(self.slider.bars[1]["Ids"][2], fill="white")

        self.submitbutton = ttk.Button(
            self.window,
            text=Text().submit[ProfileHandler().get_attribute("language")],
            command=self.submit,
        )
        self.resetbutton = ttk.Button(
            self.window,
            text=Text().reset[ProfileHandler().get_attribute("language")],
            command=self.reset,
        )
        self.spacer = tk.Label(self.window, text="")
        self.submitbutton.grid(row=0, column=3, sticky="NW")
        self.resetbutton.grid(row=0, column=1, sticky="NE")
        self.spacer.grid(row=1, column=2)
        self.slider.grid(row=2, column=0, columnspan=5, sticky="S")

        self.a = slidervars[0].trace("w", self.update)
        self.b = slidervars[1].trace("w", self.update)
        self.stay_on_top()

        self.starttime = time.time()

    def update(self, *args):

        if time.time() > self.starttime + 0.1:
            self.parent.canvas.pack_forget()
            self.parent.refresh()
            self.parent.canvas.pack(side=tk.TOP, fill="both", expand=True)
            self.starttime = time.time()
        return

    def submit(self):
        self.parent.slidervars[0].trace_vdelete("w", self.a)
        self.parent.slidervars[1].trace_vdelete("w", self.b)
        self.parent.xlimmenu = False
        self.parent.parent.bind("<MouseWheel>", self.parent.change_x_limits)
        self.window.destroy()
        self.parent.refresh()
        return

    def reset(self):
        self.parent.current_limits = self.parent.initial_limits
        self.parent.slidervars[0].set(self.parent.initial_limits[0])
        self.parent.slidervars[1].set(self.parent.initial_limits[1])
        self.slider.destroy()
        self.slider = None
        self.slider = RangeSliderH(
            self.window,
            variables=self.parent.slidervars,
            padX=100,
            valueSide="BOTTOM",
            Width=500,
            min_val=self.parent.current_limits[0],
            max_val=self.parent.current_limits[1],
            font_family="Helvetica",
            font_size=12,
            digit_precision=".0f",
            suffix=" mm",
        )
        self.slider.grid(row=1, column=0, columnspan=2, sticky="N")
        self.submit()
        return

    def stay_on_top(self):

        if self.parent.dark.get() != self.dark:
            self.dark = self.parent.dark.get()
            if self.dark == True:
                self.slider.canv.configure(bg="#363636")
                self.slider.canv.itemconfigure(
                    self.slider.bars[0]["Ids"][2], fill="white"
                )
                self.slider.canv.itemconfigure(
                    self.slider.bars[1]["Ids"][2], fill="white"
                )
            else:
                self.slider.canv.configure(bg="#ffffff")
                self.slider.canv.itemconfigure(
                    self.slider.bars[0]["Ids"][2], fill="black"
                )
                self.slider.canv.itemconfigure(
                    self.slider.bars[1]["Ids"][2], fill="black"
                )

        self.new_geometry = [
            self.parent.parent.winfo_rootx(),
            self.parent.parent.winfo_rooty(),
            self.parent.winfo_width(),
            self.parent.winfo_height(),
        ]
        self.window.lift()
        self.window.after(50, self.stay_on_top)
        if self.new_geometry == self.geometry:
            return

        self.geometry = self.new_geometry
        self.window.geometry(
            f"{500}x{self.height}+{int(self.geometry[0]+self.geometry[2]//2) - 250}+{int(self.geometry[1]+self.geometry[3]//2)}"
        )
