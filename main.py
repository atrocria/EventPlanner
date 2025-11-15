import tkinter as tk
from tkinter import ttk

def convert():
    mile_input = entry_int.get()
    km_output = mile_input * 1.61
    output_string.set(km_output)

window = tk.Tk()
window.title('Demo')  # fixed typo
window.geometry('300x150')

style = ttk.Style()
style.theme_use("clam")

# Set a global background color for the window
window.configure(background="#ffffff")

# Make ttk labels match the window
style.configure("TLabel", background="#ffffff")

# Make ttk frames match the window
style.configure("TFrame", background="#ffffff")

# Make ttk entries match too
style.configure("TEntry", fieldbackground="#ffffff", background="#ffffff")

style.configure(
    "Blue.TButton",
    background="#fab84e",
    foreground="black",
    padding=6
)

style.map(
    "Blue.TButton",
    background=[("active", "#fab84e")],
    foreground=[("active", "white")]
)

title_label = ttk.Label(window, text='chatbox', font='Calibri 24 bold', justify='center')
title_label.pack()

input_frame = ttk.Frame(window)

entry_int = tk.IntVar()
entry = ttk.Entry(input_frame, textvariable=entry_int)

button = ttk.Button(input_frame, text='Convert', style="Blue.TButton", command=convert)

entry.pack(side='left')
button.pack(side='left')
input_frame.pack(pady=10)

output_string = tk.StringVar()
output_label = ttk.Label(window, text='Output', font='Calibri 24', textvariable=output_string)
output_label.pack(pady=10)

window.mainloop()
