import os
import tkinter as tk
from customtkinter import CTkFrame, CTkButton, CTkCanvas

class SidebarUI(CTkFrame):
    def __init__(self, parent, menu_items=None, splash_callback=None, show_callback=None, width=100):
        super().__init__(parent, width=width)
        self.parent = parent
        self.configure(width=width)
        self.splash_callback = splash_callback
        self.show_callback = show_callback
        self.menu_items = menu_items or []
        self.images = {} # keep references to image objects

        # keep original size for size bar
        self.grid_propagate(False)
        self.columnconfigure(0, weight=1)

        # frame for the icons to rearange
        self.buttons_frame = CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=1, column=0, sticky="n", padx=2, pady=6)
        
        # selection state + colors, None for default
        self.selected_index = None
        self.selected_fg = ("#FF9C43", "#FF9C43")
        self.selected_hover = ("#FFB07A", "#FFB07A")
        self.unselected_fg = ("#D9D9D9", "#D9D9D9")
        self.unselected_hover = ("#FFB07A", "#FFB07A")

        self.buttons = []
        for idx, item in enumerate(self.menu_items):
            canvas, circle = self.create_icon_button(self.buttons_frame, item, idx)
            canvas.grid(row=idx, column=0, pady=8)
            self.buttons.append({"canvas": canvas,"circle": circle, "target": item.get("target")})

        self.rowconfigure(99, weight=1)
        
        info_btn = CTkButton(
            self,
            text="ⓘ",
            width=40,
            height=40,
            fg_color="transparent",
            font=("Helvetica", 15, "bold"),
            text_color="white",
            command=self.splash_callback
        )
        info_btn.grid(row=100, column=0, pady=10, sticky="w")

        if self.buttons:
            self.on_click(0)
        
    def create_icon_button(self, parent, item, idx):
        # label = item.get("name", f"item{idx}")
        icon_path = item.get("icon")
        # target = item.get("target")

        image_obj = None
        if icon_path and os.path.exists(icon_path):
            # put button and resize into circle button
            image_obj = tk.PhotoImage(file=icon_path)
            self.images[f"{icon_path}_{idx}"] = image_obj
            
        # make the circle button
        canvas_button = CTkCanvas(
            parent,
            width=69,
            height=69,
            highlightthickness=0,
            bg="#1f1f1f"
        )
        canvas_button.grid(row=idx, column=0, pady=0)
            
        # circle where icon sits, acts as a button
        circle = canvas_button.create_oval(2, 2, 67, 67, fill=self.unselected_fg[0], outline="", tags=("nav_btn",)) # tuple for better readability
        if image_obj:
            icon = canvas_button.create_image(34, 34, image=image_obj, tags=("nav_btn",))          # image
        else:
            icon = canvas_button.create_text(34, 34, text="err", fill="black", tags=("nav_btn",))  # fallback

        canvas_button.tag_bind("nav_btn", "<Button-1>", lambda e, i=idx: self.on_click(i))
        canvas_button.tag_bind(
            "nav_btn", "<Enter>", 
            lambda e, i=idx: self.on_nav_enter(canvas_button, circle, i)
        )
        canvas_button.tag_bind(
            "nav_btn", "<Leave>", 
            lambda e, i=idx: self.on_nav_leave(canvas_button, circle, i)
        )
            
        return canvas_button, circle
        
        
    def on_nav_enter(self, canvas, circle, index):
        # hover color only if NOT selected
        if self.selected_index != index:
            canvas.itemconfigure(circle, fill=self.unselected_hover[0])

        # always change cursor
        canvas.configure(cursor="hand2")

    def on_nav_leave(self, canvas, circle, index):
        # revert only if NOT selected
        if self.selected_index != index:
            canvas.itemconfigure(circle, fill=self.unselected_fg[0])

        # reset cursor
        canvas.configure(cursor="")

    def on_click(self, index):
        # valid index check
        if index < 0 or index >= len(self.buttons):
            return

        self.select(index)
        
        target_frame = self.buttons[index]["target"]
        if self.show_callback and target_frame:
            self.show_callback(target_frame, getattr(target_frame, "splash_key", None))
        else:
            print("No target/frame assigned / no show_callback given.")
            
    def select(self, index):
        if index < 0 or index >= len(self.buttons):
            return
        
        if index == self.selected_index:
            return

        if self.selected_index is not None:
            old_btn = self.buttons[self.selected_index]
            old_btn["canvas"].itemconfigure(old_btn["circle"], fill=self.unselected_fg[0])
            
        new_btn = self.buttons[index]
        new_btn["canvas"].itemconfigure(new_btn["circle"], fill=self.selected_fg[0])
        
        self.selected_index = index
        
    def select_by_target(self, target_frame):
        for idx, btn in enumerate(self.buttons):
            if btn["target"] is target_frame:
                self.select(idx)
                return