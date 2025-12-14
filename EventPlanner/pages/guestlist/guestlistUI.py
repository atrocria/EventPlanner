import customtkinter                as ctk
from customtkinter                  import CTkFrame
from tkinter                        import messagebox, simpledialog
from .guestlistController           import GuestController

class GuestListUI(CTkFrame):
    def __init__(self, parent, controller: GuestController, back_target):
        super().__init__(parent)

        self.controller = controller
        self.back_target = back_target

        self.place(relx=0.5, rely=0.5, anchor="center")

        # Header
        ctk.CTkLabel(self, text="GUEST LIST MANAGER", font=("Segoe UI", 32, "bold")).pack(pady=(0, 5))
        self.guest_count_label = ctk.CTkLabel(self, text="Total Guests: 0", font=("Segoe UI", 20, "italic"))
        self.guest_count_label.pack(pady=(0, 10))

        FORM_WIDTH = 540

        # Guest Name
        ctk.CTkLabel(self, text="Guest Name:", font=("Segoe UI", 22)).pack(anchor="w")
        self.name_entry = ctk.CTkEntry(self, width=FORM_WIDTH, height=45)
        self.name_entry.pack(pady=(0, 10))

        # RSVP
        ctk.CTkLabel(self, text="RSVP Status:", font=("Segoe UI", 22)).pack(anchor="w")
        self.rsvp_var = ctk.StringVar(value="Yes")
        self.rsvp_dropdown = ctk.CTkComboBox(
            self,
            values=["Yes", "No"],
            variable=self.rsvp_var,
            width=FORM_WIDTH,
            height=45,
            state="readonly"
        )
        self.rsvp_dropdown.pack(pady=(0, 20))

        # Buttons
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack()

        ctk.CTkButton(btns, text="ADD GUEST", command=self.add_guest).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btns, text="VIEW GUEST LIST", command=self.show_guests).grid(row=0, column=1, padx=10)
        ctk.CTkButton(btns, text="REMOVE GUEST", command=self.remove_guest).grid(row=1, column=0, padx=10, pady=10)
        ctk.CTkButton(btns, text="CLEAR FORM", command=self.clear_form).grid(row=1, column=1, padx=10, pady=10)

        self.status_label = ctk.CTkLabel(parent, text="Ready.", font=("Segoe UI", 16))
        self.status_label.place(relx=0.5, rely=0.98, anchor="center")

        self.refresh_guest_count(0)

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
        guests = self.controller.get_guest()
        if not guests:
            self.update_status("No guests added yet.")
            return

        text = "\n".join(f"- {g.name} (RSVP: {g.rsvp})" for g in guests)
        messagebox.showinfo("Guest List", f"Total Guests: {len(guests)}\n\n{text}")

    def remove_guest(self):
        guests = self.controller.get_guest()
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
            count = len(self.controller.get_guests())
        self.guest_count_label.configure(text=f"Total Guests: {count}")

    def update_status(self, message):
        self.status_label.configure(text=message)
