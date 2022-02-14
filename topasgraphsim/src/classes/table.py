import tkinter as tk


class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        t = SimpleTable(self, 10, 2)
        t.pack(side="top", fill="x")
        t.set(0, 0, "Hello, world")


class SimpleTable(tk.Frame):
    def __init__(self, parent, rows=10, columns=2):
        # use black background so it "peeks through" to
        # form grid lines
        tk.Frame.__init__(self, parent, bg="white")
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = tk.Label(
                    self, borderwidth=0, width=10, font=("DejaVu Sans", 13)
                )
                label.grid(
                    row=row, column=column, sticky="nsew", padx=1, pady=1,
                )
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def set(self, row, column, value, fontsize):
        widget = self._widgets[row][column]
        widget.configure(text=value, font= ("DejaVu Sans", fontsize))
