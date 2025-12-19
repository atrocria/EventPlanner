# dependencies / external libraries
import os
import json
import customtkinter                      as ctk
from customtkinter                        import CTk

# side bar and dashboard
from pages.sidebarUI                      import SidebarUI
from pages.dashboardUI                    import DashboardUI
from pages.dashboardController            import DashboardController
from pages.splash                         import SplashUI, SplashState

# task manager
from pages.tasks.taskUI                   import TaskUI
from pages.tasks.taskController           import TaskController
from pages.tasks.tasksServices            import TaskServices

# guest manager
from pages.guestlist.guestlistUI          import GuestListUI
from pages.guestlist.guestlistController  import GuestController
from pages.guestlist.guestlistService     import GuestListService

# budget manager
from pages.budget.budgetUI                import BudgetUI
from pages.budget.budgetController        import BudgetController
from pages.budget.budgetServices          import BudgetService

# final countdown manager
from pages.countdown.countdownService     import CountdownService
from pages.countdown.countdownController  import CountdownController
from pages.countdown.countdownUI          import CountdownUI

def show_frame(frame, splash_key=None):
    frame.tkraise()

    # refresh stuff in dashboard
    if hasattr(frame, "refresh") and callable(frame.refresh):
      frame.refresh()

    if splash_key and splash_key in SPLASHES:
      if not splash_state.has_seen(splash_key):
        cfg = SPLASHES[splash_key]
        SplashUI(
          root, 
          title=cfg["title"], 
          message=cfg["message"], 
          image_path=os.path.join(BASE_DIR, cfg.get("image", "")), 
          on_close=lambda: splash_state.mark_seen(splash_key)
        )
        
# check file for first launch, splash screen
def is_first_launch():
  flag = os.path.join(BASE_DIR, ".first_launch")
  if not os.path.exists(flag):
    with open(flag, "w") as f:
      f.write("first_splash_shown\n")
      return True
    return False
  
def on_splash_close():
  root.attributes("-alpha", 1.0)
  
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
root.minsize(window_width, window_height)

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
with open(os.path.join(BASE_DIR, "pages", "splash", "splashes.json"), "r") as f:
  SPLASHES = json.load(f)
  
def show_page_splash(splash_key):
  if splash_key not in SPLASHES:
    return
  
  cfg = SPLASHES[splash_key]
  SplashUI(
    root,
    title=cfg["title"],
    message=cfg["message"],
    image_path=os.path.join(BASE_DIR, cfg.get("image", "")),
    on_close=None
  )
root.show_page_splash = show_page_splash
splash_state = SplashState(BASE_DIR)

# configure how menu should be arranged
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=1)

countdown_service = CountdownService()
countdown_controller = CountdownController(countdown_service)

task_service = TaskServices(file_path=os.path.join(BASE_DIR, "pages", "tasks", "tasks.json"), countdown_service=countdown_service)
task_controller = TaskController(task_service)

budget_service = BudgetService()
budget_controller = BudgetController(budget_service)

guestlist_service = GuestListService(file_path=os.path.join(BASE_DIR, "pages", "guestlist", "guests.json"))
guestlist_controller = GuestController(guestlist_service)

# dashboard page
dashboard_controller = DashboardController(
  countdown_service=countdown_service, 
  budget_service=budget_service, 
  tasks_service=task_service, 
  guestlist_service=guestlist_service
  )
dashboard = DashboardUI(root, controller=dashboard_controller) 

# countdown page
countdown_menu = CountdownUI(root, controller=countdown_controller, back_target=dashboard, splash_key="countdown")

# tasks page
task_menu = TaskUI(root, controller=task_controller, back_target=dashboard, splash_key="tasks")

# budget page
budget_menu = BudgetUI(root, controller=budget_controller, back_target=dashboard, splash_key="budget")

# guest manager page
guestlist_menu = GuestListUI(root, controller=guestlist_controller, back_target=dashboard, splash_key="guestlist")

# UI -> controller -> service <- model
# for each menu option, align into column
for frame in (
  dashboard,
  guestlist_menu,
  task_menu,
  budget_menu,
  countdown_menu
  ):
  frame.grid(row=0, column=1, sticky="nsew")
  
# for sidebar
Menu = [
  {"name": "Dashboard", "icon": os.path.join(icon_path, "dashboard.png"), "target": dashboard},
  {"name": "Countdown", "icon": os.path.join(icon_path, "countdown.png"), "target": countdown_menu},
  {"name": "Tasks",     "icon": os.path.join(icon_path, "tasks.png"),     "target": task_menu},
  {"name": "Budget",    "icon": os.path.join(icon_path, "budget.png"),    "target": budget_menu},
  {"name": "Guests",    "icon": os.path.join(icon_path, "guests.png"),    "target": guestlist_menu}
]

# side bar selector
sidebar = SidebarUI(root, menu_items=Menu, splash_callback=lambda:show_app_splash(root), show_callback=show_frame)
sidebar.grid(row=0, column=0, sticky="ns")
root.sidebar = sidebar

# show dashboard first
show_frame(dashboard)
if is_first_launch():
  root.after(150, lambda: show_app_splash(root=root))
  
def show_app_splash(root):
    root.attributes("-alpha", 0.95)

    def on_close():
        root.attributes("-alpha", 1.0)

    SplashUI(root, title="Welcome", message="Plan events without losing your mind.", image_path=os.path.join(BASE_DIR, "icons", "black_hole_rose.png"), on_close=on_close)

# game start
root.mainloop()