import customtkinter as ctk
from customtkinter import CTkButton, CTkLabel

root = ctk.CTk()
root.title("Event Planner")
root.geometry("430x500")
ctk.set_appearance_mode("Dark")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=0)
root.columnconfigure(2, weight=1)

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)

spacer = ctk.CTkFrame(root, width=50)
spacer.grid(row=0, column=0, sticky="nesw")
spacer1 = ctk.CTkFrame(root, width=2)
spacer1.grid(row=0, column=2, sticky="nesw")

CTkButton(root, text="ok man").grid(row=0, column=1)

root.mainloop()