from customtkinter  import CTkToplevel, CTkFrame, CTkLabel, CTkButton
from tkinter        import PhotoImage, Label, TclError
import os

class SplashState:
    def __init__(self, base_dir):
        self.file = os.path.join(base_dir, ".first_launch")
        self.seen = self.load()

    def load(self):
        if not os.path.exists(self.file):
            return set()
        with open(self.file, "r") as f:
            return set(line.strip() for line in f if line.strip())

    def has_seen(self, key):
        # if this returns true, then the splash screen for the module has been seen
        return key in self.seen

    def mark_seen(self, key):
        if key not in self.seen:
            self.seen.add(key)
            with open(self.file, "a") as f:
                f.write(key + "\n")

class SplashUI(CTkToplevel):
    def __init__(self, parent, title, message, image_path, on_close=None):
        super().__init__(parent)

        self.on_close = on_close
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.title = title
        self.message = message
        self.resizable(False, False)

        # splash size
        width, height = 800, 500
        self.center_on_screen(width, height)

        # ---------- BACKGROUND ----------
        self.bg_image = None

        if image_path and os.path.exists(image_path):
            try:
                self.bg_image = PhotoImage(file=image_path)
                self.bg_image = self.bg_image.subsample(2, 2)
                bg = Label(self, image=self.bg_image)
            except TclError:
                bg = CTkFrame(self, fg_color="#1e1e1e")
        else:
            bg = CTkFrame(self, fg_color="#1e1e1e")

        bg.place(relx=0, rely=0, relwidth=1, relheight=1)

        # ---------- CONTENT ----------
        content = CTkFrame(self, width=320, fg_color="#1e1e1e", height=220, corner_radius=20)
        content.place(relx=0.5, rely=0.5, anchor="center")
        content.pack_propagate(False)

        CTkLabel(
            content,
            text=self.title,
            font=("Segoe UI", 22, "bold"),
            text_color="#FF9C43"
        ).pack(pady=(30, 0))
        
        CTkLabel(
            content,
            text=self.message,
            font=("Segoe UI", 15, "bold"),
            wraplength=300
        ).pack(pady=(5, 0))

        CTkButton(
            content,
            text="Let's go!",
            command=self.close
        ).pack(pady=(25, 0))
        
        support_label = CTkLabel(
            content,
            text="Support us!",
            text_color="#4ea1ff",
            font=("Segoe UI", 12, "underline"),
            cursor="hand2"
        )
        support_label.pack(side="bottom", pady=(4, 0))

        support_label.bind("<Button-1>", lambda e: self.support_links())
        
        def on_enter(e):
            support_label.configure(text_color="#79b8ff")

        def on_leave(e):
            support_label.configure(text_color="#4ea1ff")

        support_label.bind("<Enter>", on_enter)
        support_label.bind("<Leave>", on_leave)

        # ---------- SAFETY ----------
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.after(100, lambda: self.focus_force())
        self.after(100, lambda: self.attributes("-topmost", False))
        self.grab_set()

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
