# dependencies / external libraries
import  os
import  customtkinter
from    customtkinter           import CTk

# side bar and dashboard
from pages.sidebarUI            import SidebarUI
from pages.dashboardUI          import DashboardUI

# task manager
from pages.taskUI               import TaskUI
from pages.taskController       import TaskController
from pages.tasksServices        import TaskServices

# guest manager (MVC)
# from pages.guestlistUI          import GuestListUI
# from pages.guestlistController  import GuestController
# from pages.guestlistService     import GuestListService
# from pages.guestlistModel       import Guest

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

# guest manager page
# guest_service = GuestListService()
# guest_controller = GuestController(guest_service)
# guest_menu = GuestListUI(root, controller=guest_controller, back_target=dashboard, title="Guest Manager")

#tasks page
task_controller = TaskController(TaskServices())
task_menu = TaskUI(root, controller=task_controller, back_target=dashboard, title="Tasks")

#budget page
budget_controller = BudgetController(BudgetService())
budget_menu = BudgetUI(root, controller=budget_controller, back_target=dashboard)

# countdown_menu = CountdownUI(root)

# UI -> controller -> service <- model
# for each menu option, align into column
for frame in (
  dashboard,
  # guest_menu,
  task_menu,
  budget_menu,
  # countdown_menu
  ):
  frame.grid(row=0, column=1, sticky="nsew")
  
Menu = [
  {"name": "Dashboard", "icon": os.path.join(icon_path, "dashboard.png"), "target": dashboard},
  # {"name": "Guests",    "icon": os.path.join(icon_path, "guests.png"),    "target": guest_menu},
  {"name": "Tasks",     "icon": os.path.join(icon_path, "tasks.png"),     "target": task_menu},
  {"name": "Budget",    "icon": os.path.join(icon_path, "budget.png"),    "target": budget_menu}
  # {"name": "Countdown", "icon": os.path.join(icon_path, "countdown.png"), "target": countdown_menu},
]

# side bar selector
sidebar = SidebarUI(root, menu_items=Menu, show_callback=show_frame, title="menu_bar")
sidebar.grid(row=0, column=0, sticky="ns")

#showing the stuff starting with dashboard
show_frame(dashboard)
root.mainloop()
