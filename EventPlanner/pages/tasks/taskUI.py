import tkinter          as tk
import customtkinter    as ctk
import datetime
from customtkinter      import CTkFrame, CTkEntry, CTkButton, CTkLabel, CTkCheckBox, CTkScrollableFrame, CTkFont, BooleanVar
from .taskController    import TaskController
from .tasksServices     import TaskNotificationService
from .tasksModel        import TaskModel
from .tasktimeUI        import TaskTimeUI

#TODO: due date, send button

class TaskItem(CTkFrame):
    def __init__(self, parent, *, controller, task: TaskModel, on_delete, on_edited, on_toggled, sync_order):
        super().__init__(parent, fg_color="#202020", corner_radius=6)
        
        # task element consists: id, text, done_bool.
        # tasks can be deleted, edited, checked, and dynamically resized by changing of window size
        self.controller = controller
        self.task = task
        self.on_delete = on_delete
        self.on_edited = on_edited
        self.on_toggled = on_toggled
        self.sync_order = sync_order
        self.edit_entry = None
        self.resize_cooldown = None
        self.normal_bg = "#202020"
        self.delete_bg = "#3a1f1f" 
        
        # bulk delete var
        self.delete_var = BooleanVar(value=False)
        self.delete_var.trace_add("write", self.on_delete_toggle)
        self.delete_box = None
        
        # config for each task which goes inside tasks_box
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.normal_font = CTkFont(family="Arial", size=15)
        self.strike_font = CTkFont(family="Arial", size=15)
        self.strike_font.configure(overstrike=1)

        self.label = CTkLabel(self, text=task.text, anchor="w", justify="left", wraplength=1200, font=self.normal_font, cursor="hand2")
        self.label.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        
        # show due time if exists
        if self.task.due_at:
            due_str = self.task.due_at.strftime("%Y-%m-%d %H:%M")
            self.label.configure(text=f"{self.task.text}\n⏱ {due_str}")

        # if the task is done, add strikethrough
        if task.done:
            self.label.configure(font=self.strike_font, text_color="gray70")
        
        # when the window is being resized, change the length of the text inside the label
        self.bind("<Configure>", self.on_resize)
        
        # double click to edit the tasks
        self.label.bind("<Double-Button-1>", self.start_edit)
        
        self.drag_start_y = 0
        self.dragging = False

        self.label.bind("<ButtonPress-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.on_drag)
        self.label.bind("<ButtonRelease-1>", self.end_drag)
        
        # checkbox button
        self.check_var = ctk.BooleanVar(value=task.done)
        self.check_box = CTkCheckBox(self, text=None, command=self.checked, variable=self.check_var, onvalue=True, offvalue=False, width=24)
        self.check_box.grid(row=0, column=0, padx=5, pady=5)

        # kabab button, yum view more stuff
        self.task_option = CTkButton(self, text="⋮", font=CTkFont("Helvetica", 25, "bold"), text_color="white", fg_color=self.normal_bg, hover_color="#101010", corner_radius=15, command=self.toggle_taskme)
        self.task_option.grid(row=0, column=2, sticky="e")
        
        
        # task menu stats
        self.menu_open = False
        self.menu_can_close = False
        self.menu_debounce_ms = 150
        self.winfo_toplevel().bind("<Button-1>", self.on_global_click, add="+")
        
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

        CTkButton(
            self.menu_frame,
            text="⏱ Set Time",
            anchor="w",
            command=self.open_time_ui
        ).pack(fill="x", padx=8, pady=4)

    def start_drag(self, event):
        # if in bulk delete mode, outta here
        if self.check_box.cget("state") == "disabled":
            return
        
        self.drag_start_y = event.y_root
        self.dragging = True
        self.lift()
        
    def on_drag(self, event):
        if not self.dragging:
            return

        parent = self.master  # tasks_box
        y = event.y_root

        for widget in parent.winfo_children():
            if widget == self:
                continue
            wy = widget.winfo_rooty()
            wh = widget.winfo_height()

            if wy < y < wy + wh:
                self._swap_with(widget)
                break
            
    def _swap_with(self, other):
        my_row = int(self.grid_info()["row"])
        other_row = int(other.grid_info()["row"])

        if my_row == other_row:
            return

        self.grid(row=other_row)
        other.grid(row=my_row)

    def end_drag(self, event):
        if not self.dragging:
            return

        self.dragging = False
        self.sync_order()

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

        self.menu_frame.place(
            x=bx - tx - 120,
            y=by - ty + bh
        )

        self.menu_frame.tkraise()
        self.menu_frame.lift()

        self.menu_open = True
        self.after(self.menu_debounce_ms, self._enable_menu_close)
    
    def _enable_menu_close(self):
        self.menu_can_close = True
        
    def open_time_ui(self):
        self.menu_frame.place_forget()
        self.menu_open = False

        TaskTimeUI(
            parent=self.winfo_toplevel(),
            task=self.task,
            on_save=self.on_time_set,
            anchor_seconds=self.controller.get_anchor_seconds()
        )
        
    def on_time_set(self, due_at: datetime.datetime): #! controller persist due_at
        self.task.due_at = due_at
        print(f"Task {self.task.id} → {self.task.due_at}")
        
        if isinstance(self.task.due_at, datetime.datetime):
            due_str = self.task.due_at.strftime("%Y-%m-%d %H:%M")
            self.label.configure(text=f"{self.task.text}\n⏱ {due_str}")
        self.on_edited(self.task.id, self.task.text)
    
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
        self.menu_frame.place_forget()

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
        
        if not self.menu_can_close:
            return
        
        # True = click location is inside widget
        if self.clicked_location_compare(event, self.task_option):
            return
        
        if self.clicked_location_compare(event, self.menu_frame):
            return

        # If click is outside its task row and its menu, close it
        self.menu_frame.place_forget()
        self.menu_open = False
        self.menu_can_close = False
    
    # check clicked widget and compare 
    def clicked_location_compare(self, event, widget):
        clicked_widget = self.winfo_toplevel().winfo_containing(event.x_root, event.y_root)
        
        while clicked_widget:
            if clicked_widget == widget:
                return True
            clicked_widget = clicked_widget.master
        return False

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
        self.header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
        self.header.grid_columnconfigure(0, weight=0)  # title + info
        self.header.grid_columnconfigure(1, weight=1)  # spacer
        self.header.grid_columnconfigure(2, weight=0)  # bulk delete
        self.header.grid_columnconfigure(3, weight=0)  # info button

        self.title_label = CTkLabel(
            self.header,
            text="Tasks",
            font=CTkFont("Helvetica", 35, "bold"),
            anchor="w"
        )
        self.title_label.grid(row=0, column=0, sticky="w")
        
        self.tasks_info_label = CTkLabel(
            self.header,
            text="",
            text_color="gray70",
            font=CTkFont("Helvetica", 14),
            anchor="w"
        )
        self.tasks_info_label.grid(row=1, column=0, sticky="w", pady=(4, 0))

        # info button
        CTkButton(
            self.header,
            text="ⓘ",
            width=30,
            command=lambda: self.winfo_toplevel().show_page_splash(self.splash_key)
        ).grid(row=0, column=3, rowspan=2, sticky="e", padx=(10, 0))
        
        self.bulk_delete_button = CTkButton(
            self.header,
            text="🗑 Bulk Delete",
            width=50,
            corner_radius=10,
            fg_color="#2D1616",
            hover_color="#D74E4E",
            text_color="#bbbbbb",
            border_width=1,
            border_color="#ff6c6c",
            command=self.toggle_bulk_delete_mode
        )
        self.bulk_delete_button.grid(row=0, column=2, rowspan=2, sticky="e")

        # --- task box area ---
        self.task_and_entry = CTkFrame(
            self,
            fg_color="#282828",
            corner_radius=12
        )
        self.task_and_entry.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        self.task_and_entry.grid_columnconfigure(0, weight=1)
        self.task_and_entry.grid_rowconfigure(0, weight=1)  # tasks
        self.task_and_entry.grid_rowconfigure(1, weight=0)  # entry

        self.tasks_box = CTkScrollableFrame(
            self.task_and_entry,
            fg_color="transparent",
            corner_radius=0
        )
        self.tasks_box.grid(row=0, column=0, sticky="nsew", padx=12, pady=(12, 6))
        self.tasks_box.grid_columnconfigure(0, weight=1)

        # entry for posts, pressing enter post the tasks to top
        self.task_entry = CTkFrame(self.task_and_entry, fg_color="transparent")
        self.task_entry.grid(row=1, column=0, sticky="ew", padx=12, pady=(6, 12))

        self.task_entry.grid_columnconfigure(0, weight=1)
        self.task_entry.grid_columnconfigure(1, weight=0)

        self.entry = CTkEntry( #! change
            self.task_entry, 
            fg_color="transparent",
            text_color="#bbbbbb",
            border_width=1,
            border_color="#555555", 
            placeholder_text="psst.. add your task here"
        )
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self.on_enter_post)
        
        self.post_button = CTkButton(self.task_entry, text="post", command=self.on_enter_post)
        self.post_button.grid(row=0, column=1, sticky="e")

        # back button (required)
        self.back_button = CTkButton(
            self,
            text="← Back to Dashboard",
            command=self.go_back,
            width=180,
            height=38,
            fg_color="transparent",
            hover_color="#3a3a3a",
            text_color="#bbbbbb",
            border_width=1,
            border_color="#555555",
            corner_radius=10
        )
        self.back_button.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        for task in self.controller.get_task():
            self.add_task_widget(task)
            
        self.notification_service = TaskNotificationService(
            controller=self.controller,
            on_notify=self.notify_task
        )

        self.start_due_date_checker()

        self.update_tasks_display()
            
    def go_back(self):
        self.back_target.tkraise()

        root = self.winfo_toplevel()
        if hasattr(root, "sidebar"):
            root.sidebar.select_by_target(self.back_target)

        if hasattr(self.back_target, "refresh"):
            self.back_target.refresh()

    # tell controller check th f up
    def on_task_toggled(self, task_id):
        self.controller.toggle_task(task_id)
        self.update_tasks_display()
        
    # make a task, tell taskItem to deal with it, and store it in a dict
    def add_task_widget(self, task: TaskModel):
        index = len(self.framedTasks)
        item = TaskItem(
            self.tasks_box,
            task=task,
            controller=self.controller,
            on_delete=self.on_task_deletion,
            on_edited=self.on_task_edit,
            on_toggled=self.on_task_toggled,
            sync_order=self.sync_task_order
        )
        item.grid(row=index, column=0, sticky="ew", padx=5, pady=5)
        self.framedTasks[task.id] = item
    
    def on_enter_post(self, event=None):
        text = self.entry.get().strip()
        if not text:
            return
        
        task = self.controller.add_task(text)
        self.add_task_widget(task)
        self.update_tasks_display()
            
        self.entry.delete(0, "end")
        
    def on_task_deletion(self, task_id):
        self.controller.delete_task(task_id)
        widget = self.framedTasks.pop(task_id)
        widget.destroy()
        self._regrid_tasks()
        self.update_tasks_display()

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
        self.update_tasks_display()
        
        # exit delete mode and delete duty
        self.bulk_delete_cancel()
    
    def on_delete_select(self, task_id, selected):
        if selected:
            self.delete_selection[task_id] = self.controller.get_task_by_id(task_id)
        else:
            self.delete_selection.pop(task_id, None)
            
        self.update_bulk_delete_button()
    
    # tell controller, see TaskItem
    def on_task_edit(self, task_id, new_text):
        self.controller.update_task(task_id, new_text)
        
    def sync_task_order(self):
        ordered = sorted(
            self.framedTasks.items(),
            key=lambda kv: kv[1].grid_info()["row"]
        )
        ordered_ids = [task_id for task_id, _ in ordered]
        self.controller.reorder_tasks(ordered_ids)

    # re-configure task alignment
    def _regrid_tasks(self):
        ordered = sorted(
            self.framedTasks.items(),
            key=lambda kv: kv[1].grid_info()["row"]
        )
        for row, (task_id, widget) in enumerate(ordered):
            widget.grid_configure(row=row)

    # readonly
    def disable_task_input(self):
        self.entry.configure(state="disabled", fg_color="#3a1f1f")
        self.post_button.configure(state="disabled", fg_color="#3a1f1f")

    def enable_task_input(self):
        self.entry.configure(state="normal", fg_color="#343638")
        self.post_button.configure(state="normal", fg_color="#D6D6D6")

    # escape button logic
    def on_escape_pressed(self, event=None):
        if self.bulk_delete_mode:
            self.bulk_delete_cancel()
            self.update_bulk_delete_button()
            return "break"
        
    def update_tasks_display(self):
        info = self.controller.get_tasks_info()

        if not info["has_tasks"]:
            self.tasks_info_label.configure(text="No tasks yet")
            return

        self.tasks_info_label.configure(
            text=f"{info['pending']} pending • {info['completed']} done"
        )

    def start_due_date_checker(self):
        self.check_due_dates()

    def check_due_dates(self):
        self.notification_service.check()
        self.after(30_000, self.check_due_dates)

        
    def notify_task(self, task: TaskModel):
        popup = ctk.CTkToplevel(self)
        popup.title("⏰ Task Due")
        popup.geometry("360x160")
        popup.attributes("-topmost", True)

        label = CTkLabel(
            popup,
            text=f"Task due:\n\n{task.text}",
            font=CTkFont("Helvetica", 16, "bold"),
            wraplength=320,
            justify="center"
        )
        label.pack(padx=20, pady=20)

        CTkButton(
            popup,
            text="OK",
            command=popup.destroy
        ).pack(pady=(0, 15))

def show_frame(frame):
    frame.tkraise()