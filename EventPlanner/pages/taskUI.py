import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from customtkinter import CTk,CTkFrame, CTkEntry, CTkButton

# with each enter, create a new dialog box with a checkbar on the left
# create a new dialog box that is grayed out at the bottom of the last task
# make a delete task button, interactable?

#add task, edit task, delete task, mark tasks, due date
#services controllers state machines

#! set limit to 10
class TaskUI(CTkFrame):
    def __init__(self, parent, back_target, title="untitled"):
        super().__init__(parent)
        self.back_target = back_target

        # make this frame use grid internally
        self.rowconfigure(0, weight=1)   # task box grows
        self.rowconfigure(1, weight=0)   # entry
        self.rowconfigure(2, weight=0)   # back button
        self.columnconfigure(0, weight=1)

        # --- task box area ---
        self.tasks_box = CTkFrame(self, fg_color="#202020", corner_radius=10)
        self.tasks_box.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # later you'll add task rows INSIDE self.tasks_box

        # --- entry under the box ---
        self.entry = CTkEntry(self, placeholder_text="psst.. add your task here")
        self.entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.entry.bind("<Return>", self.on_enter_post)

        # --- back button at the bottom ---
        self.back_button = CTkButton(
            self,
            text="Back",
            width=25,
            command=lambda: show_frame(self.back_target)
        )
        self.back_button.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))

    def on_enter_post(self, event=None):
        print("posted")
        # here you'll eventually create a task widget inside self.tasks_box

def show_frame(frame):
    frame.tkraise()