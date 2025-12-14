from pages.countdownService import CountdownService
from pages.budgetServices   import BudgetService
from pages.tasksServices    import TaskServices
from pages.guestlistService import GuestListService

#display cards, communicate with each component's services for info
class DashboardController():
    def __init__(self, countdown_service: CountdownService, budget_service: BudgetService, tasks_service: TaskServices, guestlist_service: GuestListService):
        self.countdown_service = countdown_service
        self.budget_service = budget_service
        self.tasks_service = tasks_service
        self.guestlist_service = guestlist_service
        print("sup")

    def get_countdown_info():
        pass
        
    def get_budget_info():
        pass

    def get_guestlist_info():
        pass

    def get_tasks_info():
        pass