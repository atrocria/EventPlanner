import customtkinter as ctk
from customtkinter import CTk,CTkFrame, CTkEntry, CTkButton, CTkLabel, CTkCheckBox, CTkScrollableFrame, CTkFont
from pages.taskController import TaskController
from pages.tasksModel import TaskModel

# with each enter, create a new dialog box with a checkbar on the left
# create a new dialog box that is grayed out at the bottom of the last task
# make a delete task button, interactable?

#add task, edit task, delete task, mark tasks, due date
#services controllers state machines

class TaskItem(CTkFrame):
    def __init__(self, parent, task: TaskModel, on_delete, on_edited, on_toggled):
        super().__init__(parent, fg_color="#2a2a2a", corner_radius=6)
        self.task = task
        self.on_delete = on_delete
        self.on_edited = on_edited
        self.on_toggled = on_toggled
        self.edit_entry = None
        self.resize_cooldown = None
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.normal_font = CTkFont(family="Arial", size=15)
        self.strike_font = CTkFont(family="Arial", size=15)
        self.strike_font.configure(overstrike=1)

        self.label = CTkLabel(self, text=task.text, anchor="w", justify="left", wraplength=1200, font=self.normal_font)
        self.label.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        
        if task.done:
            self.label.configure(font=self.strike_font, text_color="gray70")
        
        self.bind("<Configure>", self.on_resize)
        
        # double click to edit using bind
        self.label.bind("<Double-Button-1>", self.start_edit)
        
        # checkbox button
        self.check_var = ctk.BooleanVar(value=task.done)
        self.check_box = CTkCheckBox(self, text=None, command=self.checked, variable=self.check_var, onvalue=True, offvalue=False, width=24)
        self.check_box.grid(row=0, column=0, padx=5, pady=5)

        # delete button
        self.delete_button = CTkButton(self, text="X", width=40, command=lambda: self.on_delete(self.task.id))
        self.delete_button.grid(row=0, column=2, padx=5, pady=5)
    
    # check if in cooldown, go to apply resize function
    def on_resize(self, event):
        if self.resize_cooldown:
            self.after_cancel(self.resize_cooldown)

        # start timer
        self.resize_cooldown = self.after(100, self.apply_wrap)
    
    # resizing
    def apply_wrap(self):
        self.resize_cooldown = None
        
        new_width = max(self.winfo_width() - 120, 100)
        self.label.configure(wraplength=new_width)
    
    def checked(self):
        is_on = self.check_var.get()
        
        if is_on:
            self.label.configure(font=self.strike_font, text_color="gray70")
        else:
            self.label.configure(font=self.normal_font, text_color="white")
        
        self.on_toggled(self.task.id)
            
        print("done =", self.task.done)
    
    def start_edit(self, event=None):
        # hide the label
        self.label.grid_remove()

        # make an entry with the current text
        self.edit_entry = CTkEntry(self, width=250)
        self.edit_entry.insert(0, self.task.text)
        self.edit_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        # focus on entry
        self.edit_entry.focus()

        # finish / cancel edit scenario
        self.edit_entry.bind("<Return>", self.finish_edit)
        
    def finish_edit(self, event=None):
        if not self.edit_entry:
            return
        
        edited_text = self.edit_entry.get().strip()
        if edited_text and edited_text != self.task.text:
            self.task.text = edited_text
            self.label.configure(text=edited_text)
            
            # tell controller about the change
            self.on_edited(self.task.id, edited_text)

        # delete entry and show the label with the new text
        self.edit_entry.destroy()
        self.edit_entry = None
        self.label.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

    def cancel_edit(self, event=None):
        if not self.edit_entry:
            return

        self.edit_entry.destroy()
        self.edit_entry = None
        self.label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

#! set limit to 10
class TaskUI(CTkFrame):
    def __init__(self, parent, controller: TaskController, back_target, title="untitled"):
        super().__init__(parent)
        self.controller = controller
        self.back_target = back_target
        
        # all created task items stored here
        self.framedTasks: dict[str, TaskItem] = {}

        self.columnconfigure(0, weight=1)   # left space grows

        # make this frame use grid internally
        self.rowconfigure(0, weight=1)   # task box
        self.rowconfigure(1, weight=0)   # entry
        self.rowconfigure(2, weight=0)   # back button

        # --- task box area ---
        self.tasks_box = CTkScrollableFrame(self, fg_color="#202020", corner_radius=10)
        self.tasks_box.grid(row=0, column=0, sticky="nsew", padx=50, pady=30)
        self.tasks_box.grid_columnconfigure(0, weight=1)

        # entry for posts, pressing enter post the tasks to top
        self.entry = CTkEntry(self, placeholder_text="psst.. add your task here")
        self.entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.entry.bind("<Return>", self.on_enter_post)

        # back button (required)
        self.back_button = CTkButton(
            self,
            text="Back",
            width=25,
            command=lambda: show_frame(self.back_target)
        )
        self.back_button.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        for task in self.controller.get_task():
            self.add_task_widget(task)
            
    def on_task_toggled(self, task_id):
        self.controller.toggle_task(task_id)
        
    def add_task_widget(self, task: TaskModel):
        index = len(self.framedTasks)
        item = TaskItem(
            self.tasks_box,
            task,
            on_delete=self.on_task_deletion,
            on_edited=self.on_task_edit,
            on_toggled=self.on_task_toggled,
        )
        item.grid(row=index, column=0, sticky="ew", padx=5, pady=5)
        self.framedTasks[task.id] = item
    
    def on_enter_post(self, event=None):
        text = self.entry.get().strip()
        if not text:
            return
        
        task = self.controller.add_task(text)
        self.add_task_widget(task)
            
        self.entry.delete(0, "end")
        print("posted")
        
    def on_task_deletion(self, task_id):
        self.controller.delete_task(task_id)
        widget = self.framedTasks.pop(task_id)
        widget.destroy()
        self._regrid_tasks()
    
    # tell controller, see TaskItem
    def on_task_edit(self, task_id, new_text):
        self.controller.update_task(task_id, new_text)

    # re-configure task alignment
    def _regrid_tasks(self):
        for row, task_id in enumerate(self.framedTasks):
            self.framedTasks[task_id].grid_configure(row=row)

def show_frame(frame):
    frame.tkraise()