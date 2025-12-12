# guestlistUI.py
import customtkinter as ctk
from guestlistController import GuestController

class GuestListUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Planner")
        self.root.geometry("1440x788")

        container = ctk.CTkFrame(root, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Header
        ctk.CTkLabel(container, text="GUEST LIST MANAGER", font=("Segoe UI", 32, "bold")).pack(pady=(0, 5))
        self.guest_count_label = ctk.CTkLabel(container, text="Total Guests: 0", font=("Segoe UI", 20, "italic"))
        self.guest_count_label.pack(pady=(0, 10))

        FORM_WIDTH = 540

        # Guest Name block
        name_block = ctk.CTkFrame(container, fg_color="transparent")
        name_block.pack(pady=5)
        ctk.CTkLabel(name_block, text="Guest Name:", font=("Segoe UI", 22)).pack(anchor="w", pady=(0, 3))
        self.name_entry = ctk.CTkEntry(name_block, width=FORM_WIDTH, height=45, placeholder_text="Enter guest name...")
        self.name_entry.pack()

        # RSVP Status block
        rsvp_block = ctk.CTkFrame(container, fg_color="transparent")
        rsvp_block.pack(pady=(15, 5))
        ctk.CTkLabel(rsvp_block, text="RSVP Status:", font=("Segoe UI", 22)).pack(anchor="w", pady=(0, 3))
        self.rsvp_var = ctk.StringVar(value="Yes")
        self.rsvp_dropdown = ctk.CTkComboBox(rsvp_block, values=["Yes", "No"], variable=self.rsvp_var,
                                             width=FORM_WIDTH, height=45, state="readonly")
        self.rsvp_dropdown.pack()

        # Buttons
        btn_card = ctk.CTkFrame(container, fg_color="transparent")
        btn_card.pack(pady=20)

        button_style = {
            "width": 260,
            "height": 55,
            "fg_color": "#3A6EA5",
            "hover_color": "#ff8800",
            "corner_radius": 12,
            "font": ("Segoe UI", 18)
        }

        self.controller = GuestController(self)

        ctk.CTkButton(btn_card, text="ADD GUEST", command=lambda: self.controller.add_guest(self.name_entry.get(), self.rsvp_var.get()), **button_style).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(btn_card, text="VIEW GUEST LIST", command=self.controller.view_guests, **button_style).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(btn_card, text="REMOVE GUEST", command=self.controller.remove_guest, **button_style).grid(row=1, column=0, padx=10, pady=10)
        ctk.CTkButton(btn_card, text="CLEAR FORM", command=self.controller.clear_form, **button_style).grid(row=1, column=1, padx=10, pady=10)

        # Status bar
        self.status_label = ctk.CTkLabel(root, text="Ready.", font=("Segoe UI", 16), text_color="#cccccc")
        self.status_label.place(relx=0.5, rely=0.98, anchor="center")

    # UI helper methods
    def update_status(self, message):
        self.status_label.configure(text=message)

    def refresh_guest_count(self, count):
        self.guest_count_label.configure(text=f"Total Guests: {count}")

    def clear_form(self):
        self.name_entry.delete(0, "end")
        self.rsvp_var.set("Yes")
        self.rsvp_dropdown.focus()
