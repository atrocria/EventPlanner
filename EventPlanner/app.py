#dependencies
import  datetime
#import  tkinter         as tk
from    tkinter         import ttk, messagebox, simpledialog
import customtkinter
from    customtkinter   import CTk, CTkInputDialog, CTkButton, CTkLabel

#import pages
from pages.dashboardUI      import DashboardUI
from pages.taskUI           import TaskUI
# from pages.guestlist      import GuestList
# from pages.calculator     import Calculator
# from pages.timer          import Timer

#! remove
guests = []
budget_items = []
budget_limit = 0

def show_frame(frame):
    frame.tkraise()

# -------------------------
# Dashboard menu                                   #!make separate into a frame side panel
# -------------------------

#root main window setup + darkmode
root = CTk()
root.title("Event Planner")
root.geometry("430x500")
customtkinter.set_appearance_mode("Dark")

#configure how menu should be arranged
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

#! side bar section
#sidebar = ttk.Frame(self, width=80)
#sidebar.grid(row=0, column=0, sticky="ns")
#sidebar.grid_propagate(False)

#setting up page names
dashboard = DashboardUI(root)
# guest_menu = GuestList(root)
task_menu = TaskUI(root, back_target=dashboard, title="hello from app")
# budget_menu = Calculator(root)

#displaying each option
#! need refactoring
for frame in (dashboard, 
            #   guest_menu, 
              task_menu, 
            #   budget_menu
              ):
    frame.grid(row=0, column=0, sticky="nsew")

CTkLabel(dashboard, text="EVENT PLANNER", font=("Arial", 18, "bold")).pack(pady=20)
    
CTkButton(dashboard, text="Dashboard", width=25, command=lambda: DashboardUI.pinging()).pack(pady=5)
# CTkButton(dashboard, text="Guest Manager", width=25, command=lambda: show_frame(GuestList)).pack(pady=5)
CTkButton(dashboard, text="Task Checklist", width=25, command=lambda: show_frame(task_menu)).pack(pady=5)
# CTkButton(dashboard, text="Budget Tracker", width=25, command=lambda: show_frame(Calculator)).pack(pady=5)
# CTkButton(dashboard, text="Countdown", width=25, command=Timer).pack(pady=5)
CTkButton(dashboard, text="Exit", width=25, command=root.quit).pack(pady=20)

#showing the stuff starting with dashboard
show_frame(dashboard)
root.mainloop()