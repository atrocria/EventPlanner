import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.title('getting and setting widgets')
window.geometry('800x500')

def func():
    label['text'] = entry.get()
    entry['state'] = 'disabled'

def reset():
    label['text'] = 'reset'
    entry['state'] = 'enabled'

label = ttk.Label(master=window, text='label')
label.pack()

entry = ttk.Entry(master=window)
entry.pack()

button = ttk.Button(master=window, text='a button to retrieve', command=func)
button.pack()

buttonanother = ttk.Button(master=window, text='a button to reset', command=reset)
buttonanother.pack()

window.mainloop()