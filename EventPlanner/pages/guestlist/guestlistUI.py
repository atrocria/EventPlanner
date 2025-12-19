import customtkinter                as ctk
from customtkinter                  import CTkFrame
from tkinter                        import messagebox, simpledialog
from .guestlistController           import GuestController

import customtkinter                as ctk
from customtkinter                  import CTkFrame
from tkinter                        import messagebox, simpledialog
from .guestlistController           import GuestController

class GuestListUI(CTkFrame):
    def __init__(self, parent, controller: GuestController, back_target, splash_key="guestlist"):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.back_target = back_target
        self.splash_key = splash_key

        # ---- layout: use grid inside this frame ----
        # configure columns so the form sits centered in column 1
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        # HEADER (left title, right info button)
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=3, sticky="ew", padx=20, pady=(10, 8))
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)

        ctk.CTkLabel(header, text="GUEST LIST MANAGER", font=("Segoe UI", 32, "bold")) \
            .grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            header,
            text="ⓘ",
            width=30,
            command=lambda: self.winfo_toplevel().show_page_splash(self.splash_key)
        ).grid(row=0, column=1, sticky="e", padx=(10,0))

        # guest count under header (centered across the frame)
        self.guest_count_label = ctk.CTkLabel(self, text="Total Guests: 0", font=("Segoe UI", 20, "italic"))
        self.guest_count_label.grid(row=1, column=0, columnspan=3, pady=(0, 12))

        FORM_WIDTH = 540

        # Guest Name label + entry (put in center column)
        ctk.CTkLabel(self, text="Guest Name:", font=("Segoe UI", 22)) \
            .grid(row=2, column=1, sticky="w", padx=(0,10))
        self.name_entry = ctk.CTkEntry(self, width=FORM_WIDTH, height=45)
        self.name_entry.grid(row=3, column=1, pady=(6, 12))

        # RSVP label + combo
        ctk.CTkLabel(self, text="RSVP Status:", font=("Segoe UI", 22)) \
            .grid(row=4, column=1, sticky="w", padx=(0,10))
        self.rsvp_var = ctk.StringVar(value="Yes")
        self.rsvp_dropdown = ctk.CTkComboBox(
            self,
            values=["Yes", "No"],
            variable=self.rsvp_var,
            width=FORM_WIDTH,
            height=45,
            state="readonly"
        )
        self.rsvp_dropdown.grid(row=5, column=1, pady=(6, 18))

        # Buttons container (keeps button grid grouped)
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.grid(row=6, column=1)

        # Use self.* methods (not controller.*) for view/remove/add/clear
        ctk.CTkButton(btns, text="ADD GUEST", command=self.add_guest) \
            .grid(row=0, column=0, padx=10, pady=4)
        ctk.CTkButton(btns, text="VIEW GUEST LIST", command=self.show_guests) \
            .grid(row=0, column=1, padx=10, pady=4)
        ctk.CTkButton(btns, text="REMOVE GUEST", command=self.remove_guest) \
            .grid(row=1, column=0, padx=10, pady=6)
        ctk.CTkButton(btns, text="CLEAR FORM", command=self.clear_form) \
            .grid(row=1, column=1, padx=10, pady=6)

        # status label — kept as you had it (attached to parent with place)
        self.status_label = ctk.CTkLabel(parent, text="Ready.", font=("Segoe UI", 16))
        self.status_label.place(relx=0.5, rely=0.98, anchor="center")
        
        bottom_bar = ctk.CTkFrame(self, fg_color="transparent")
        bottom_bar.grid(row=99, column=0, columnspan=3, pady=(20, 10), sticky="s")

        # make sure the layout can push content up
        self.grid_rowconfigure(99, weight=1)

        ctk.CTkButton(
            bottom_bar,
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
        ).pack()

        # initialize count
        self.refresh_guest_count(0)
        
    def go_back(self):
        if not self.back_target:
            return

        # show dashboard
        self.back_target.tkraise()

        # sync sidebar highlight
        root = self.winfo_toplevel()
        if hasattr(root, "sidebar"):
            root.sidebar.select_by_target(self.back_target)

        # refresh dashboard if needed
        if hasattr(self.back_target, "refresh"):
            self.back_target.refresh()

    # ---------- UI Actions ----------
    def add_guest(self):
        try:
            guest, count = self.controller.add_guest(
                self.name_entry.get(),
                self.rsvp_var.get()
            )
            messagebox.showinfo("Guest Added", f"{guest.name} added.")
            self.update_status("Guest added.")
            self.refresh_guest_count(count)
            self.clear_form()

        except Exception as e:
            self.update_status(str(e))

    def show_guests(self):
        # use the controller method that returns the list of guests
        # original code had get_guest vs get_guests; prefer get_guests for consistency
        guests = self.controller.get_guests() if hasattr(self.controller, "get_guests") else self.controller.get_guests()
        if not guests:
            self.update_status("No guests added yet.")
            return

        text = "\n".join(f"- {g.name} (RSVP: {g.rsvp})" for g in guests)
        messagebox.showinfo("Guest List", f"Total Guests: {len(guests)}\n\n{text}")

    def remove_guest(self):
        guests = self.controller.get_guests() if hasattr(self.controller, "get_guests") else self.controller.get_guests()
        if not guests:
            self.update_status("No guests to remove.")
            return

        names = [g.name for g in guests]
        choice = simpledialog.askstring("Remove Guest", f"Enter guest name:\n{', '.join(names)}")
        if not choice:
            return

        try:
            guest, count = self.controller.remove_guest(choice)
            messagebox.showinfo("Guest Removed", f"{guest.name} removed.")
            self.refresh_guest_count(count)
            self.update_status("Guest removed.")
        except Exception as e:
            self.update_status(str(e))

    def clear_form(self):
        self.name_entry.delete(0, "end")
        self.rsvp_var.set("Yes")
        self.name_entry.focus()

    # ---------- Helpers ----------
    def refresh_guest_count(self, count=None):
        if count is None:
            # prefer get_guests, fallback to get_guest if that's what controller exposes
            guests = self.controller.get_guests() if hasattr(self.controller, "get_guests") else self.controller.get_guests()
            count = len(guests)
        self.guest_count_label.configure(text=f"Total Guests: {count}")

    def update_status(self, message):
        self.status_label.configure(text=message)
