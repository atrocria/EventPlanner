import customtkinter as ctk
from customtkinter import CTk,CTkFrame, CTkEntry, CTkButton, CTkLabel

# with each enter, create a new dialog box with a checkbar on the left
# create a new dialog box that is grayed out at the bottom of the last task
# make a delete task button, interactable?

#add task, edit task, delete task, mark tasks, due date
#services controllers state machines

class TaskItem(CTkFrame):
    def __init__(self, parent, task, on_delete):
        super().__init__(parent, fg_color="#2a2a2a", corner_radius=6)
        self.task = task
        self.on_delete = on_delete
        
        self.grid_columnconfigure(0, weight=1)

        self.label = CTkLabel(self, text=task.text)
        self.label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.delete_button = CTkButton(self, text="X", width=40, command=lambda: self.on_delete(self.task.id))
        self.delete_button.grid(row=0, column=1, padx=5, pady=5)

#! set limit to 10
class TaskUI(CTkFrame):
    def __init__(self, parent, controller, back_target, title="untitled"):
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
        self.tasks_box = CTkFrame(self, fg_color="#202020", corner_radius=10)
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
        
        #where all the taks live in a dict
        # self.framedTasks = []
        
        for task in self.controller.get_task():
            self.add_task_widget(task)
        
    # see self.entry.bind("<Return>", self.on_enter_post)
    def on_enter_post(self, event=None):
        text = self.entry.get().strip()
        if not text:
            return
        
        task = self.controller.add_task(text)
        index = len(self.framedTasks)
        item = TaskItem(self.tasks_box, task, on_delete=self.on_task_deletion)
        item.grid(row=index, column=0, sticky="ew", padx=5, pady=5)
        self.framedTasks[task.id] = item
            
        # self.tasks.append(item)
        self.entry.delete(0, "end")
        print("posted")
        
    def on_task_deletion(self, task_id):
        self.controller.delete_task(task_id)
        widget = self.framedTasks.pop(task_id)
        widget.destroy()
        self._regrid_tasks()

    def _regrid_tasks(self):
        for row, task_id in enumerate(self.framedTasks):
            self.framedTasks[task_id].grid_configure(row=row)

def show_frame(frame):
    frame.tkraise()