import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from customtkinter import CTk,CTkFrame

# with each enter, create a new dialog box with a checkbar on the left
# create a new dialog box that is grayed out at the bottom of the last task
# make a delete task button, interactable?

#add task, edit task, delete task, mark tasks, due date

class Tasks(CTkFrame):
    def __init__(self, parent, title="untitled"):
        super().__init__(parent)
        
        def on_enter_post():
            print("posted")
    
        task = []
        
        entry = CTk.Entry(self)
        entry.pack()

        entry.bind("<Return>", on_enter_post)

        
    
    