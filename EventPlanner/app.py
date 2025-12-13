# dependencies / external libraries
import  os
import  customtkinter           as ctk
from    customtkinter           import CTk

# side bar and dashboard
from pages.sidebarUI            import SidebarUI
from pages.dashboardUI          import DashboardUI
from pages.splashUI             import SplashUI

# task manager
from pages.taskUI               import TaskUI
from pages.taskController       import TaskController
from pages.tasksServices        import TaskServices

# guest manager (MVC)
from pages.guestlistUI          import GuestListUI
from pages.guestlistController  import GuestController
from pages.guestlistService     import GuestListService

# budget manager
from pages.budgetUI             import BudgetUI
from pages.budgetController     import BudgetController
from pages.budgetServices       import BudgetService

# final countdown manager
from pages.countdownService     import CountdownService
from pages.countdownController  import CountdownController
from pages.countdownUI          import CountdownUI

def show_frame(frame):
    frame.tkraise()
    
# check file for first launch, splash screen
def is_first_launch():
  flag = os.path.join(BASE_DIR, ".first_launch")
  if not os.path.exists(flag):
    with open(flag, "w") as f:
      f.write("shown")
      return True
    return False
  
# center the app on the screen
def center_window(window, width, height, x, y):
  window.geometry(f"{width}x{height}+{x}+{y}")

# -------------------------
# Dashboard menu           
# -------------------------

# root main window setup + darkmode
root = CTk()
root.title("Event Planner")
root.update_idletasks()

# calculate the center of the screen
window_width = 1200
window_height = 800
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
center_x = (screen_w // 2) - (window_width // 2)
center_y = (screen_h // 2) - (window_height // 2)
center_window(root, window_width, window_height, center_x, center_y)

# file should be at the same level as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# set to dark mode, use custom theme and set file_dir
ctk.set_appearance_mode("Dark")
icon_path = os.path.join(BASE_DIR, "icons")
app_icon = os.path.join(icon_path, "app_icon.ico")

root.iconbitmap(app_icon)
ctk.set_default_color_theme(os.path.join(BASE_DIR, "theme.json"))

# configure how menu should be arranged
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=1)

# dashboard page
dashboard = DashboardUI(root)

# guest manager page
guest_controller = GuestController(GuestListService())
guest_menu = GuestListUI(root, controller=guest_controller, back_target=dashboard)

# tasks page
task_controller = TaskController(TaskServices())
task_menu = TaskUI(root, controller=task_controller, back_target=dashboard)

# budget page
budget_controller = BudgetController(BudgetService())
budget_menu = BudgetUI(root, controller=budget_controller, back_target=dashboard)

# countdown page
countdown_controller = CountdownController(CountdownService())
countdown_menu = CountdownUI(root, controller=countdown_controller, back_target=dashboard)

# UI -> controller -> service <- model
# for each menu option, align into column
for frame in (
  dashboard,
  guest_menu,
  task_menu,
  budget_menu,
  countdown_menu
  ):
  frame.grid(row=0, column=1, sticky="nsew")
  
# for sidebar
Menu = [
  {"name": "Dashboard", "icon": os.path.join(icon_path, "dashboard.png"), "target": dashboard},
  {"name": "Countdown", "icon": os.path.join(icon_path, "countdown.png"), "target": countdown_menu},
  {"name": "Budget",    "icon": os.path.join(icon_path, "budget.png"),    "target": budget_menu},
  {"name": "Tasks",     "icon": os.path.join(icon_path, "tasks.png"),     "target": task_menu},
  {"name": "Guests",    "icon": os.path.join(icon_path, "guests.png"),    "target": guest_menu}
]

# side bar selector
sidebar = SidebarUI(root, menu_items=Menu, show_callback=show_frame)
sidebar.grid(row=0, column=0, sticky="ns")

#showing the stuff starting with dashboard
show_frame(dashboard)
if is_first_launch():
  root.after(150, lambda: SplashUI(root))
  
# game start
root.mainloop()