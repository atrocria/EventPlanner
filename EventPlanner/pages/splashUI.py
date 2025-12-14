from customtkinter import CTkToplevel, CTkFrame, CTkLabel, CTkButton
from tkinter import PhotoImage, Label, TclError
import os

class SplashUI(CTkToplevel):
    def __init__(self, parent, file_path, on_close=None):
        super().__init__(parent)

        self.on_close = on_close
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.title("Welcome")
        self.resizable(False, False)

        # splash size
        width = 800
        height = 500
        self.center_on_screen(width, height)

        # ---------- BACKGROUND ----------
        self.bg_image = None
        bg_loaded = False

        if os.path.exists(file_path):
            try:
                self.bg_image = PhotoImage(file=file_path)
                self.bg_image = self.bg_image.subsample(2, 2)
                bg_loaded = True
            except TclError as e:
                print("Splash image failed to load:", e)

        if bg_loaded:
            bg = Label(
                self,
                image=self.bg_image,
                borderwidth=0,
                highlightthickness=0
            )
        else:
            # fallback if image fails
            bg = CTkFrame(self, fg_color="#282828")

        bg.place(relx=0, rely=0, relwidth=1, relheight=1)

        # ---------- CONTENT ----------
        content = CTkFrame(self, width=320, fg_color="#1e1e1e", height=220, corner_radius=20)
        content.place(relx=0.5, rely=0.5, anchor="center")
        content.pack_propagate(False)

        CTkLabel(
            content,
            text="Welcome to Event Planner",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=(0, 12))

        CTkButton(
            content,
            text="Let's go!",
            command=self.close
        ).pack(pady=30)
        
        support_label = CTkLabel(
            content,
            text="Support us!",
            text_color="#4ea1ff",
            font=("Segoe UI", 12, "underline"),
            cursor="hand2"
        )
        support_label.pack(pady=(4, 0))

        support_label.bind("<Button-1>", lambda e: self.support_links())
        
        def on_enter(e):
            support_label.configure(text_color="#79b8ff")

        def on_leave(e):
            support_label.configure(text_color="#4ea1ff")

        support_label.bind("<Enter>", on_enter)
        support_label.bind("<Leave>", on_leave)

        # ---------- SAFETY ----------
        self.transient(parent)
        self.grab_set()
        self.overrideredirect(True)

        # emergency escape
        self.bind("<Escape>", lambda e: self.close())

    def close(self):
        try:
            self.grab_release()
        except Exception:
            pass

        self.destroy()
        if self.on_close:
            self.on_close()
            
    def support_links(self):
        import webbrowser
        webbrowser.open("https://www.youtube.com/@etar")

    def center_on_screen(self, w, h):
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        x = (screen_w // 2) - (w // 2)
        y = (screen_h // 2) - (h // 2)

        self.geometry(f"{w}x{h}+{x}+{y}")
