import customtkinter as ctk
from ui.bills import BillsPage

# from dashboard import DashboardPage
# from income import IncomePage


class MultiPageApp(ctk.CTk):
    def __init__(self):
        super().__init__()  # Initialize the CTk root window (customtkinter's themed version of Tk)
        self.title("My Bill Tracker")  # Set the window title
        self.geometry("1000x700")  # Set the size of the window

        # ----- Top Navigation Bar -----
        nav_frame = ctk.CTkFrame(
            self,
            height=50,
            fg_color="black"  # Set background color to black
        )
        nav_frame.pack(side="top", fill="x")  # Fill the width of the container

        # # Navigation title (optional)
        # ctk.CTkLabel(nav_frame, text="Navigation", font=("Arial", 12, "bold"), text_color="white", bg_color="black").pack(
        #     pady=5
        # )

        # Navigation buttons for switching between pages
        dashboard_btn = ctk.CTkButton(
            nav_frame,
            text="Home",
            command=self.show_dashboard,
            fg_color="black",       # Button background color
            text_color="white",     # Button text color
            corner_radius=0,        # No rounded corners
            border_width=0          # Optional: removes border if you don't want it
    )
        dashboard_btn.pack( side="left")

        bills_btn = ctk.CTkButton(
            nav_frame,
            text="Bills",
            command=self.show_bills,
            fg_color="black",       # Button background color
            text_color="white",     # Button text color
            corner_radius=0,        # No rounded corners
            border_width=0          # Optional: removes border if you don't want it
        )
        bills_btn.pack(side="left")

        income_btn = ctk.CTkButton(
            nav_frame,
            text="Income",
            command=self.show_income,
            fg_color="black",       # Button background color
            text_color="white",     # Button text color
            corner_radius=0,        # No rounded corners
            border_width=0          # Optional: removes border if you don't want it
        )
        income_btn.pack(side="left")

        # ----- Main Page Display Area -----
        self.container = ctk.CTkFrame(
            self
        )  # Frame to hold whichever page is currently visible
        self.container.pack(side="right", fill="both", expand=True)

        # Dictionary to store the page instances
        self.pages = {}

        # ----- Page Instantiation -----
        # This dictionary maps page names to their class constructors
        page_classes = {
            "BillsPage": BillsPage,
            # "DashboardPage": DashboardPage,
            # "IncomePage": IncomePage,
        }

        for page_name, PageClass in page_classes.items():
            frame = PageClass(
                self.container
            )  # Instantiate each page with the container as the parent
            self.pages[page_name] = frame  # Store the instance in the dictionary
            frame.pack(
                fill="both", expand=True
            )  # Pack the frame so it fills the container
            frame.lower()  # Hide it initially by sending it to the back

        # Show the default page (BillsPage for now)
        self.show_bills()

    # ----- Navigation Functions -----
    def show_dashboard(self):
        """Bring the Dashboard page to the front."""
        if "DashboardPage" in self.pages:
            self.pages["DashboardPage"].lift()

    def show_bills(self):
        """Bring the Bills page to the front."""
        if "BillsPage" in self.pages:
            self.pages["BillsPage"].lift()

    def show_income(self):
        """Bring the Income page to the front."""
        if "IncomePage" in self.pages:
            self.pages["IncomePage"].lift()


# ----- Entry Point -----
if __name__ == "__main__":
    app = MultiPageApp()  # Create an instance of the app
    app.mainloop()  # Run the app's main event loop
