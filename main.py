import customtkinter as ctk
from tkinter import messagebox
#from dashboard import DashboardPage
from ui.bills import BillPage
#from income import IncomePage

class MultiPageApp(ctk.CTk):
    def __init__(self):
        super().__init__()  # Initialize the CTk root window
        self.title("Bill Tracker")  # Set the title of the application window
        self.geometry("1000x700")  # Set the initial size of the window

        # Create the navigation bar on the left side
        nav_frame = ctk.CTkFrame(self, width=200)  # Sidebar frame for navigation buttons
        nav_frame.pack(side="left", fill="y")  # Stick to the left and fill vertically

        # Navigation header label
        ctk.CTkLabel(nav_frame, text="Navigation", font=("Arial", 16, "bold")).pack(pady=20)

        # Button to switch to the Dashboard page
        dashboard_btn = ctk.CTkButton(nav_frame, text="Dashboard", command=self.show_dashboard)
        dashboard_btn.pack(pady=10)

        # Button to switch to the Bills page
        bills_btn = ctk.CTkButton(nav_frame, text="Bills", command=self.show_bills)
        bills_btn.pack(pady=10)

        # Button to switch to the Income page
        income_btn = ctk.CTkButton(nav_frame, text="Income", command=self.show_income)
        income_btn.pack(pady=10)

        # Main container to hold the active page content
        self.container = ctk.CTkFrame(self)  # This is where different page frames will be placed
        self.container.pack(side="right", fill="both", expand=True)  # Take remaining space

        # Dictionary to hold instances of the page classes
        self.pages = {}

        # Instantiate and grid each page class (Dashboard, Bills, Income)
        for Page in BillPage:
            page_name = Page.__name__  # Get class name as string
            frame = Page(self.container, self)  # Instantiate the page frame
            self.pages[page_name] = frame  # Store in dictionary
            frame.grid(row=0, column=0, sticky="nsew")  # Position it in the container frame

        # Show the dashboard page first by default
        self.show_dashboard()

    # Method to raise the DashboardPage frame
    def show_dashboard(self):
        self.pages["DashboardPage"].tkraise()

    # Method to raise the BillsPage frame
    def show_bills(self):
        self.pages["BillsPage"].tkraise()

    # Method to raise the IncomePage frame
    def show_income(self):
        self.pages["IncomePage"].tkraise()


if __name__ == "__main__":
    app = MultiPageApp()  # Create an instance of the app
    app.mainloop()  # Start the Tkinter main event loop
