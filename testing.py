import customtkinter as ctk
from customtkinter import CTkButton, CTkLabel

root = ctk.CTk()
root.title("Event Planner")
root.geometry("430x500")
ctk.set_appearance_mode("Dark")

label = CTkLabel(root, text="haha")
label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

# double click to edit using bind
label.bind("<Double-Button-1>", lambda e: print("double"))

root.mainloop()