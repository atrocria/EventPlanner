from customtkinter import CTk,CTkFrame, CTkButton

#display cards, communicate with each component's services for info
class DashboardUI(CTkFrame):
    def __init__(self, parent, title="untitled"):
        super().__init__(parent)
        CTkButton(self, text="Dashboard").pack()
       
    def pinging(): 
        print("fuck")