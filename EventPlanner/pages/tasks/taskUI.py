import customtkinter    as ctk
from customtkinter      import CTkFrame, CTkEntry, CTkButton, CTkLabel, CTkCheckBox, CTkScrollableFrame, CTkFont, BooleanVar
from .taskController    import TaskController
from .tasksModel        import TaskModel

#TODO: due date, send button

# refers to the individual task
class TaskItem(CTkFrame):
    def __init__(self, parent, task: TaskModel, on_delete, on_edited, on_toggled):
        super().__init__(parent, fg_color="#202020", corner_radius=6)
        
        # task element consists: id, text, done_bool.
        # tasks can be deleted, edited, checked, and dynamically resized by changing of window size
        self.task = task
        self.on_delete = on_delete
        self.on_edited = on_edited
        self.on_toggled = on_toggled
        self.edit_entry = None
        self.resize_cooldown = None
        self.normal_bg = "#202020"
        self.delete_bg = "#3a1f1f" 
        
        # bulk delete var
        self.delete_var = BooleanVar(value=False)
        self.delete_var.trace_add("write", self.on_delete_toggle)
        self.delete_box = None
        
        # close task menu
        self.menu_can_close = False
        self.winfo_toplevel().bind("<Button-1>", self.on_global_click, add="+")
        
        # config for each task which goes inside tasks_box
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.normal_font = CTkFont(family="Arial", size=15)
        self.strike_font = CTkFont(family="Arial", size=15)
        self.strike_font.configure(overstrike=1)

        self.label = CTkLabel(self, text=task.text, anchor="w", justify="left", wraplength=1200, font=self.normal_font)
        self.label.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        
        # if the task is done, add strikethrough
        if task.done:
            self.label.configure(font=self.strike_font, text_color="gray70")
        
        # when the window is being resized, change the length of the text inside the label
        self.bind("<Configure>", self.on_resize)
        
        # double click to edit the tasks
        self.label.bind("<Double-Button-1>", self.start_edit)
        
        # checkbox button
        self.check_var = ctk.BooleanVar(value=task.done)
        self.check_box = CTkCheckBox(self, text=None, command=self.checked, variable=self.check_var, onvalue=True, offvalue=False, width=24)
        self.check_box.grid(row=0, column=0, padx=5, pady=5)

        # kabab button, yum view more stuff
        self.task_option = CTkButton(self, text="⋮", font=CTkFont("Helvetica", 25, "bold"), text_color="white", fg_color=self.normal_bg, hover_color="#101010", corner_radius=15, command=self.toggle_taskme)
        self.task_option.grid(row=0, column=2)
        
        self.menu_open = False
        
        self.menu_frame = CTkFrame(
            self.winfo_toplevel(),
            fg_color=self.normal_bg,
            corner_radius=10,
            border_width=1,
            border_color="#444444"
        )
        
        CTkButton(
            self.menu_frame,
            text="🗑 Delete",
            anchor="w",
            command=self.confirm_delete
        ).pack(fill="x", padx=8, pady=4)

        CTkButton(
            self.menu_frame,
            text="✏ Edit",
            anchor="w",
            command=self.start_edit
        ).pack(fill="x", padx=8, pady=4)

    # menu toggle
    def toggle_taskme(self):
        if self.menu_open:
            self.menu_frame.place_forget()
            self.menu_open = False
            return

        self.menu_frame.update_idletasks()
        
        bx = self.task_option.winfo_rootx()
        by = self.task_option.winfo_rooty()
        bh = self.task_option.winfo_height()

        tx = self.winfo_toplevel().winfo_rootx()
        ty = self.winfo_toplevel().winfo_rooty()

        print("MENU PARENT:", self.menu_frame.master)
        self.menu_frame.place(
            x=bx - tx - 120,
            y=by - ty + bh
        )
        print("MAPPED:", self.menu_frame.winfo_ismapped())
        print(
            "PLACE AT:",
            bx - tx - self.menu_frame.winfo_width(),
            by - ty + bh
        )

        self.menu_frame.lift()
        self.menu_frame.tkraise()
        self.menu_frame.lift(self.winfo_toplevel())

        self.menu_open = True
        self.after(100, self._enable_menu_close)
        print("reached")
    
    def _enable_menu_close(self):
        self.menu_can_close = True
        
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
    
    # on delete duty, only disable and show "delete task" checkbox
    def enable_delete_mode(self, callback):
        # disable the "task done" button
        self.check_box.configure(state="disabled")

        # make a "delete task" checkbox
        if not self.delete_box:
            self.delete_box = CTkCheckBox(
                self, 
                text="🗑",
                variable=self.delete_var, # boolean
                command=lambda: callback(self.task.id, self.delete_var.get()), # calls on_delete_select()
                width=24,
                fg_color="#ff3b3b",
                hover_color="#ff6b6b",
                text_color="#ff3b3b"
            )
            self.delete_box.grid(row=0, column=0, padx=5, pady=5)
            
    # out of delete duty, delete the "delete task" checkbox and re-enable "task done" button
    def disable_delete_mode(self):
        # delete the "delete task" checkbox, if it exist
        if self.delete_box:
            self.delete_box.destroy()
            self.delete_box = None
            self.delete_var.set(False)
        
        # enable "task done" button
        self.configure(fg_color=self.normal_bg)
        self.check_box.configure(state="normal")
    
    def on_delete_toggle(self, *args):
        if self.delete_var.get():
            self.configure(fg_color=self.delete_bg)
        else:
            self.configure(fg_color=self.normal_bg)
    
    # delete for task menu
    def confirm_delete(self):
        self.menu_frame.place_forget()
        self.menu_open = False
        self.on_delete(self.task.id)
    
    # is the task checked?
    def checked(self):
        is_on = self.check_var.get()
        
        if is_on:
            self.label.configure(font=self.strike_font, text_color="gray70")
        else:
            self.label.configure(font=self.normal_font, text_color="white")
        
        # toggle the task by communicating to the controller, see on_task_toggled
        self.on_toggled(self.task.id)
    
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
        self.edit_entry.bind("<FocusOut>", self.cancel_edit)
        self.edit_entry.bind("<Escape>", self.cancel_edit)
        
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
        self.label.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

    def on_global_click(self, event):
        if not self.menu_open:
            return

        clicked_widget = self.winfo_toplevel().winfo_containing(event.x_root, event.y_root)

        # If click is outside this task row and its menu, close it
        if clicked_widget not in (self.menu_frame, self.task_option):
            self.menu_frame.place_forget()
            self.menu_open = False
            self.menu_can_close = False

class TaskUI(CTkFrame):
    def __init__(self, parent, controller: TaskController, back_target, splash_key="tasks"):
        super().__init__(parent)
        self.controller = controller
        self.back_target = back_target
        self.splash_key = splash_key
        
        self.bulk_delete_mode = False
        self.delete_selection: dict[str, TaskModel] = {}
        
        # all created task items stored here
        self.framedTasks: dict[str, TaskItem] = {}
        
        # escape logic
        self.winfo_toplevel().bind("<Escape>", self.on_escape_pressed)

        self.columnconfigure(0, weight=1)# left space grows
        self.rowconfigure(0, weight=0)   # title, info, bulk delete
        self.rowconfigure(1, weight=1)   # task box
        self.rowconfigure(2, weight=0)   # entry
        self.rowconfigure(3, weight=0)   # back button

        # BIG TITLE
        self.header = CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", padx=50, pady=(20, 0))
        self.header.grid_columnconfigure((0,1,2), weight=1)

        self.title_label = CTkLabel(
            self.header,
            text="Tasks",
            font=CTkFont("Helvetica", 35, "bold"),
            anchor="w"
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        # info button
        CTkButton(
            self,
            text="ⓘ",
            width=30,
            command=lambda: self.winfo_toplevel().show_page_splash(self.splash_key)
        ).grid(row=0, column=1, sticky="e", padx=(10,0))
        
        self.bulk_delete_button = CTkButton(
            self.header,
            text="🗑 Bulk Delete",
            width=50,
            corner_radius=12,
            fg_color="#ff6c6c",
            command=self.toggle_bulk_delete_mode
        )
        self.bulk_delete_button.grid(row=0, column=2, sticky="e")

        # --- task box area ---
        self.tasks_box = CTkScrollableFrame(self, fg_color="#282828", corner_radius=10)
        self.tasks_box.grid(row=1, column=0, sticky="nsew", padx=50, pady=30)
        self.tasks_box.grid_columnconfigure(0, weight=1)

        # entry for posts, pressing enter post the tasks to top
        self.task_entry = CTkFrame(self, fg_color="transparent")
        self.task_entry.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.task_entry.grid_columnconfigure(0, weight=1)
        self.task_entry.grid_columnconfigure(1, weight=0)
        self.entry = CTkEntry(self.task_entry, placeholder_text="psst.. add your task here")
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self.on_enter_post)
        
        self.post_button = CTkButton(self.task_entry, text="post", command=self.on_enter_post)
        self.post_button.grid(row=0, column=1, sticky="e")

        # back button (required)
        self.back_button = CTkButton(
            self,
            text="Back",
            width=25,
            command=lambda: show_frame(self.back_target)
        )
        self.back_button.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        for task in self.controller.get_task():
            self.add_task_widget(task)
            
    # tell controller check th f up
    def on_task_toggled(self, task_id):
        self.controller.toggle_task(task_id)
        
    # make a task, tell taskItem to deal with it, and store it in a dict
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
        print("task posted: UI")
        
    def on_task_deletion(self, task_id):
        self.controller.delete_task(task_id)
        widget = self.framedTasks.pop(task_id)
        widget.destroy()
        self._regrid_tasks()

    def update_bulk_delete_button(self):
        if not self.bulk_delete_mode:
            self.bulk_delete_button.configure(text="🗑 Bulk Delete")
        else:
            if self.delete_selection:
                self.bulk_delete_button.configure(text="Confirm Delete")
            else:
                self.bulk_delete_button.configure(text="Cancel")
    
    # attached to bulk delete button, toggle and disable delete mode using the same button
    def toggle_bulk_delete_mode(self):
        if not self.bulk_delete_mode:
            self.bulk_delete_mode = True
            self.delete_selection.clear()
            self.disable_task_input() # disable entry

            # for every tasks inside the container frame, make them disable check button and add a delete button
            for item in self.framedTasks.values():
                item.enable_delete_mode(self.on_delete_select)
        else:
            # if already in delete mode
            if self.delete_selection:
                self.bulk_delete_confirm()
            else:
                self.bulk_delete_cancel()
                
        # check what state the button should be in
        self.update_bulk_delete_button()
    
    def bulk_delete_cancel(self):
        self.bulk_delete_mode = False
        self.delete_selection.clear()
        self.enable_task_input() # enable entry

        # out of duty
        for item in self.framedTasks.values():
            item.disable_delete_mode()

    def bulk_delete_confirm(self):
        ids = list(self.delete_selection.keys())
        self.bulk_delete_mode = False
        self.delete_selection.clear()

        self.bulk_delete_by_ids(ids)
        
    def bulk_delete_by_ids(self, ids: list[str]):
        self.controller.delete_tasks(ids)
        
        #destroy all widgets first
        for task_id in ids:
            widget = self.framedTasks.pop(task_id, None)
            if widget:
                widget.destroy()
        
        self._regrid_tasks()
        
        # exit delete mode and delete duty
        for item in self.framedTasks.values():
            item.disable_delete_mode()
    
    def on_delete_select(self, task_id, selected):
        if selected:
            self.delete_selection[task_id] = self.controller.get_task_by_id(task_id)
        else:
            self.delete_selection.pop(task_id, None)
            
        self.update_bulk_delete_button()
    
    # tell controller, see TaskItem
    def on_task_edit(self, task_id, new_text):
        self.controller.update_task(task_id, new_text)

    # re-configure task alignment
    def _regrid_tasks(self):
        for row, task_id in enumerate(self.framedTasks):
            self.framedTasks[task_id].grid_configure(row=row)

    # readonly
    def disable_task_input(self):
        self.entry.configure(state="disabled", fg_color="#3a1f1f")
        self.post_button.configure(state="disabled", fg_color="#3a1f1f")

    def enable_task_input(self):
        self.entry.configure(state="normal", placeholder_text="psst.. add your task here", fg_color="#343638")
        self.post_button.configure(state="normal", fg_color="#D6D6D6")

    # escape button logic
    def on_escape_pressed(self, event=None):
        if self.bulk_delete_mode:
            self.bulk_delete_cancel()
            self.update_bulk_delete_button()
            return "break"

def show_frame(frame):
    frame.tkraise()