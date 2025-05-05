import customtkinter as ctk
from ui.dashboard import BillTrackerApp

if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # or "dark"
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = BillTrackerApp(root)
    root.mainloop()
