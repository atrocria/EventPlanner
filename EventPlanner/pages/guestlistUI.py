import customtkinter as ctk

def build_ui(root, guests):
    root.title("Event Planner")
    root.geometry("1440x788")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    guest_menu = ctk.CTkFrame(root)
    guest_menu.grid(row=0, column=0, sticky="nsew")
    container = ctk.CTkFrame(guest_menu, fg_color="transparent")
    container.place(relx=0.5, rely=0.44, anchor="center")

    header = ctk.CTkFrame(container, fg_color="transparent")
    header.pack(pady=(0, 10))
    ctk.CTkLabel(header, text="GUEST LIST MANAGER", font=("Segoe UI", 32, "bold")).pack()
    guest_count_label = ctk.CTkLabel(header, text=f"Total Guests: {len(guests)}", font=("Segoe UI", 20, "italic"))
    guest_count_label.pack(pady=(0, 2))

    form_card = ctk.CTkFrame(container, fg_color="#2a2a2a", corner_radius=12)
    form_card.pack(pady=20, padx=10, fill="x")

    ctk.CTkLabel(form_card, text="Guest Name:", font=("Segoe UI", 22)).pack(anchor="w", pady=(10, 5), padx=15)
    name_entry = ctk.CTkEntry(form_card, width=520, height=45)
    name_entry.pack(pady=5, anchor="w", padx=15)

    ctk.CTkLabel(form_card, text="RSVP Status:", font=("Segoe UI", 22)).pack(anchor="w", pady=(15, 5), padx=15)
    rsvp_var = ctk.StringVar(value="Yes")
    rsvp_dropdown = ctk.CTkComboBox(form_card, values=["Yes", "No"], variable=rsvp_var, width=520, height=45, state="readonly")
    rsvp_dropdown.pack(pady=5, anchor="w", padx=15)

    ctk.CTkFrame(container, height=2, fg_color="#888").pack(fill="x", pady=(25, 0))

    btn_card = ctk.CTkFrame(container, fg_color="#2a2a2a", corner_radius=12)
    btn_card.pack(pady=10, padx=10)

    button_style = {
        "width": 260,
        "height": 55,
        "fg_color": "#3A6EA5",
        "hover_color": "#ff8800",
        "corner_radius": 12,
        "font": ("Segoe UI", 18)
    }

    add_btn = ctk.CTkButton(btn_card, text="Add Guest", **button_style)
    add_btn.grid(row=0, column=0, padx=12, pady=12)
    view_btn = ctk.CTkButton(btn_card, text="View Guest List", **button_style)
    view_btn.grid(row=0, column=1, padx=12, pady=12)
    remove_btn = ctk.CTkButton(btn_card, text="Remove Guest", **button_style)
    remove_btn.grid(row=1, column=0, padx=12, pady=12)
    clear_btn = ctk.CTkButton(btn_card, text="Clear Form", **button_style)
    clear_btn.grid(row=1, column=1, padx=12, pady=12)

    ctk.CTkFrame(container, height=2, fg_color="#888").pack(fill="x", pady=(0, 10))

    status_label = ctk.CTkLabel(root, text="Ready.", font=("Segoe UI", 16), text_color="#cccccc")
    status_label.place(relx=0.5, rely=0.98, anchor="center")

    return name_entry, rsvp_var, rsvp_dropdown, guest_count_label, status_label, add_btn, view_btn, remove_btn, clear_btn
