#dependencies
import os
import customtkinter
from    customtkinter   import CTk, CTkInputDialog, CTkButton, CTkLabel, CTkFrame

#import pages
from pages.sidebarUI            import SideBarUI
from pages.dashboardUI          import DashboardUI

from pages.taskUI               import TaskUI
from pages.taskController       import TaskController
from pages.tasksServices        import TaskServices

# from pages.guestlistUI          import GuestListUI
# from pages.guestlistController  import GuestListController

# from pages.budgetUI             import BudgetUI
# from pages.budgetController     import BudgetController
# from pages.budgetServices       import BudgetService

# from pages.countdownUI    import CountdownUI

def show_frame(frame):
    frame.tkraise()

# -------------------------
# Dashboard menu                                   #!make separate into a frame side panel
# -------------------------

#root main window setup + darkmode
root = CTk()
root.title("Event Planner")
root.geometry("1200x800")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme(os.path.join(BASE_DIR, "theme.json"))

#configure how menu should be arranged
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=1)

#setting up page names
#menu bar page
sidebar = SideBarUI(root, title="menu bar")
sidebar.grid(row=0, column=0, sticky="ns")

#dashboard page
dashboard = DashboardUI(root)

#guestlist page
# guest_controller = GuestListController()
# guest_menu = GuestListUI(root, controller=guest_controller, back_target=dashboard, title="Guest Manager")

#tasks page
task_controller = TaskController(TaskServices())
task_menu = TaskUI(root, controller=task_controller, back_target=dashboard, title="hello from app")

# budget_controller = BudgetController(BudgetService())
# budget_menu = BudgetUI(root, controller=budget_controller)

#displaying each option
#! need refactoring
for frame in (dashboard, 
            # guest_menu, 
            task_menu, 
            # budget_menu
            ):
  frame.grid(row=0, column=1, sticky="nsew")

CTkLabel(dashboard, text="EVENT PLANNER", font=("Arial", 18, "bold")).pack(pady=20)
    
CTkButton(dashboard, text="Dashboard", width=25, command=lambda: DashboardUI.pinging()).pack(pady=5)
# CTkButton(dashboard, text="Guest Manager", width=25, command=lambda: show_frame(guest_menu)).pack(pady=5)
CTkButton(dashboard, text="Task Checklist", width=25, command=lambda: show_frame(task_menu)).pack(pady=5)
# CTkButton(dashboard, text="Budget Tracker", width=25, command=lambda: show_frame(budget_menu)).pack(pady=5)
# CTkButton(dashboard, text="Countdown", width=25, command=Timer).pack(pady=5)
CTkButton(dashboard, text="Exit", width=25, command=root.quit).pack(pady=20)

#showing the stuff starting with dashboard
show_frame(dashboard)
root.mainloop()
