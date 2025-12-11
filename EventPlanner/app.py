# dependencies / external libraries
import  os
import  customtkinter
from    customtkinter           import CTk, CTkButton, CTkLabel

# side bar and dashboard
from pages.sidebarUI            import SidebarUI
from pages.dashboardUI          import DashboardUI

# task manager
from pages.taskUI               import TaskUI
from pages.taskController       import TaskController
from pages.tasksServices        import TaskServices

# guestlist manager
from pages.guestlistUI          import GuestListUI
from pages.guestlistController  import GuestListController
from pages.guestlistServices    import GuestListServices

# budget manager
from pages.budgetUI             import BudgetUI
from pages.budgetController     import BudgetController
from pages.budgetServices       import BudgetService

# final countdown manager
# from pages.countdownService     import CountdownService
# from pages.countdownController  import CountdownController
# from pages.countdownUI          import CountdownUI

def show_frame(frame):
    frame.tkraise()

# -------------------------
# Dashboard menu           
# -------------------------

#root main window setup + darkmode
root = CTk()
root.title("Event Planner")
root.geometry("1200x800")

# file should be at the same level as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

customtkinter.set_appearance_mode("Dark")
icon_path = os.path.join(BASE_DIR, "icons")
app_icon = os.path.join(icon_path, "app_icon.ico")
root.iconbitmap(app_icon)
customtkinter.set_default_color_theme(os.path.join(BASE_DIR, "theme.json"))

#configure how menu should be arranged
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=1)

#dashboard page
dashboard = DashboardUI(root)

# configure pages to put inside sidebarUI
# countdown_controller = CountdownController(CountdownService())
guest_controller = GuestListController(GuestListServices())
task_controller = TaskController(TaskServices())
budget_controller = BudgetController(BudgetService())

# countdown_menu = CountdownUI(root)
guest_menu = GuestListUI(root, controller=guest_controller, back_target=dashboard, title="Guest Manager")
task_menu = TaskUI(root, controller=task_controller, back_target=dashboard, title="hello from app")
budget_menu = BudgetUI(root, controller=budget_controller, back_target=dashboard)

# UI -> controller -> service <- model

#! displaying each option, put into sidebar later
# for each menu option, align into column
for frame in (
  dashboard,
  guest_menu,
  task_menu,
  budget_menu,
  # countdown_menu
  ):
  frame.grid(row=0, column=1, sticky="nsew")
  
Menu = [
  {"name": "Dashboard", "icon": os.path.join(icon_path, "dashboard.png"), "target": dashboard},
  # {"name": "countdown", "icon": os.path.join(BASE_DIR, "icons", "countdown.png"), "target": countdown_menu},
  {"name": "Guests",    "icon": os.path.join(icon_path, "guests.png"),    "target": guest_menu},
  {"name": "Tasks",     "icon": os.path.join(icon_path, "tasks.png"),     "target": task_menu},
  {"name": "Budget",    "icon": os.path.join(icon_path, "budget.png"),    "target": budget_menu}
]

# side bar selector
sidebar = SidebarUI(root, menu_items=Menu, show_callback=show_frame, title="menu_bar")
sidebar.grid(row=0, column=0, sticky="ns")

#showing the stuff starting with dashboard
show_frame(dashboard)
root.mainloop()