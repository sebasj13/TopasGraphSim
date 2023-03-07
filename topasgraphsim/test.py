import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
import tkinterDnD  # Importing the tkinterDnD module

class Tk(ctk.CTk, tkinterDnD.dnd.DnDWrapper):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.TkDnDVersion = tkinterDnD.tk._init_tkdnd(self)

# You have to use the tkinterDnD.Tk object for super easy initialization,
# and to be able to use the main window as a dnd widget
root = Tk()  
root.title("tkinterDnD example")

stringvar = tk.StringVar()
stringvar.set('Drop here or drag from here!')


def drop(event):
    # This function is called, when stuff is dropped into a widget
    print(event.data)
    stringvar.set(event.data)
    
def drag_command(event):
    # This function is called at the start of the drag,
    # it returns the drag type, the content type, and the actual content
    return (tkinterDnD.COPY, "DND_Files", "Some nice dropped text!")


# Without DnD hook you need to register the widget for every purpose,
# and bind it to the function you want to call
label_1 = tk.Frame(root)
label_1.pack(fill="both", expand=True, padx=10, pady=10)

label_1.register_drop_target("*")
label_1.bind("<<Drop>>", drop)
label_1.register_drag_source("*")
label_1.bind("<<DragInitCmd>>", drag_command)


# With DnD hook you just pass the command to the proper argument,
# and tkinterDnD will take care of the rest
# NOTE: You need a ttk widget to use these arguments
label_2 = ttk.Label(root, ondrop=drop, ondragstart=drag_command,
                    textvar=stringvar, padding=50, relief="solid")
label_2.pack(fill="both", expand=True, padx=10, pady=10)


root.mainloop()