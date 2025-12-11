import os
import customtkinter as ctk
from customtkinter import CTkFrame, CTkButton, CTkLabel
from PIL import Image, ImageTk

class SidebarUI(CTkFrame):
    def __init__(self, parent, menu_items=None, show_callback=None, title="untitled", width=100):
        super().__init__(parent, width=width)
        self.parent = parent
        self.show_callback = show_callback
        self.menu_items = menu_items or []
        self.images = {} # keep references to image objects

        self.grid_propagate(False)
        self.columnconfigure(0, weight=1)

        self.title_label = CTkLabel(self, text=title, anchor="w")
        self.title_label.grid(row=0, column=0, padx=12, pady=(12, 6), sticky="ew")

        # frame for the icons to rearange
        self.buttons_frame = CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=1, column=0, sticky="n", padx=6, pady=6)
        
        # selection state + colors, None for default
        self.selected_index = None
        self.selected_fg = ("#FF9C43", "#FF9C43")
        self.selected_hover = ("#FFB07A", "#FFB07A")
        self.unselected_fg = None
        self.unselected_hover = None

        self.buttons = []
        for idx, item in enumerate(self.menu_items):
            btn = self.create_icon_button(self.buttons_frame, item, idx)
            btn.grid(row=idx, column=0, pady=8, padx=8, sticky="w")
            self.buttons.append({"button":btn, "target": item.get("target")})

        #! bottom spacer so sidebar doesn't stretch weirdly?
        self.rowconfigure(99, weight=1)
        
        if self.buttons:
            self.select(0)
        
    def create_icon_button(self, parent, item, idx):
        label = item.get("name", f"item{idx}")
        icon_path = item.get("icon")
        target = item.get("target")

        image_obj = None
        if icon_path and os.path.exists(icon_path):
            # put button and resize into circle button
            img = Image.open(icon_path).convert("RGBA")
            size = 30
            img = img.resize((size, size), Image.LANCZOS)
            image_obj = ImageTk.PhotoImage(img)
            self.images[f"{icon_path}_{idx}"] = image_obj
            
        # make the circle button
        btn_kwargs = dict(
            master=parent,
            text="" if image_obj else "err",
            image=image_obj,
            width=56,
            height=56,
            corner_radius=28,
            command=(lambda i=idx: self.on_click(i))
        )
        if self.unselected_fg is not None:
            btn_kwargs["fg_color"] = self.unselected_fg
        if self.unselected_hover is not None:
            btn_kwargs["hover_color"] = self.unselected_hover
        
        btn = CTkButton(**btn_kwargs)
        return btn
        
    def on_click(self, index):
        # valid index check
        if index < 0 or index >= len(self.buttons):
            return

        self.select(index)
        
        #! huh?
        target_frame = self.buttons[index]["target"]
        if self.show_callback and target_frame:
            self.show_callback(target_frame)
        else:
            print("No target/frame assigned / no show_callback given.")
            
    def select(self, index):
        if index < 0 or index >= len(self.buttons):
            return
        
        if index == self.selected_index:
            return

        if self.selected_index is not None:
            old_btn = self.buttons[self.selected_index]["button"]
            cfg = {}
            if self.unselected_fg is not None:
                cfg["fg_color"] = self.unselected_fg
            if self.unselected_hover is not None:
                cfg["hover_color"] = self.unselected_hover
            if cfg:
                old_btn.configure(**cfg)
            
        new_btn = self.buttons[index]["button"]
        new_btn.configure(fg_color=self.selected_fg, hover_color=self.selected_hover)
        
        self.selected_index = index