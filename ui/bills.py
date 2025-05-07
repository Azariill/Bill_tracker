import customtkinter as ctk
from tkinter import messagebox
from models.bill import RecurringBill
from storage.data_manager import load_bills, save_bills
from ui.widgets import create_entry_label_frame, create_button, show_error, show_info
from datetime import date
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar

class BillPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Bill Tracker")

        # Load bills from saved file
        self.bills = load_bills("data/bills.json")  # Load bills from the JSON file

        # UI Components
        self.create_widgets()

    def create_widgets(self):
        self.bill_name_var = ctk.StringVar()
        self.bill_amount_var = ctk.StringVar()  # Change to StringVar to handle validation more easily
        self.bill_frequency_var = ctk.StringVar()
        self.bill_day_var = ctk.StringVar()
        self.bill_start_date_var = ctk.StringVar()
        self.bill_end_date_var = ctk.StringVar()

        # Adding Bill Section
        add_bill_label = ctk.CTkLabel(self.root, text="Add New Bill")
        add_bill_label.pack(pady=10)

        create_entry_label_frame(self.root, "Bill Name", self.bill_name_var)
        create_entry_label_frame(self.root, "Amount", self.bill_amount_var)
        create_entry_label_frame(self.root, "Frequency (weekly/biweekly/monthly)", self.bill_frequency_var)
        create_entry_label_frame(self.root, "Day of Week", self.bill_day_var)

        # Use DateEntry for Start Date and End Date fields
        self.start_date_picker = DateEntry(self.root, textvariable=self.bill_start_date_var, date_pattern='yyyy-mm-dd')
        self.start_date_picker.pack(pady=5)

        self.end_date_picker = DateEntry(self.root, textvariable=self.bill_end_date_var, date_pattern='yyyy-mm-dd')
        self.end_date_picker.pack(pady=5)

        # Add Bill Button
        add_bill_button = create_button(self.root, "Add Bill", self.add_bill)

        # Display existing bills
        self.display_bills()

    from datetime import date

    def add_bill(self):
        # Retrieve values from input fields
        name = self.bill_name_var.get().strip()
        amount_str = self.bill_amount_var.get().strip()  # Get the amount as a string first
        frequency = self.bill_frequency_var.get().strip().lower()
        day_of_week = self.bill_day_var.get().strip().capitalize()
        start_date_str = self.bill_start_date_var.get().strip()
        end_date_str = self.bill_end_date_var.get().strip()

        # Validate amount field: check if it's a valid float
        try:
            amount = float(amount_str) if amount_str else 0.0  # If empty, set amount to 0.0
        except ValueError:
            show_error("Please enter a valid amount.")
            return

        # Validate other input fields
        if not name or amount <= 0 or frequency not in ["weekly", "biweekly",
                                                        "monthly"] or not day_of_week or not start_date_str:
            show_error("Please fill all fields correctly.")
            return

        try:
            start_date = date.fromisoformat(start_date_str)

            # If the end date is the same as today's date, set it to None
            if end_date_str == str(date.today()):
                end_date = None
            elif end_date_str:  # If an end date is provided and it's not today's date
                end_date = date.fromisoformat(end_date_str)
            else:
                end_date = None  # If no end date is provided, set to None

        except ValueError:
            show_error("Invalid date format. Use YYYY-MM-DD.")
            return

        # Create new bill and add to list
        new_bill = RecurringBill(name, amount, frequency, day_of_week, start_date, end_date)
        self.bills.append(new_bill)

        # Save updated list to file
        save_bills(self.bills, "data/bills.json")

        # Show success message and update UI
        show_info("Bill added successfully!")
        self.display_bills()

    def display_bills(self):
        # Clear existing bill labels
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()

        bills_label = ctk.CTkLabel(self.root, text="Bills:")
        bills_label.pack(pady=10)

        # Create a container frame for the table
        table_frame = ctk.CTkFrame(self.root)
        table_frame.pack(pady=5, fill="both", expand=True)

        # Header row
        header_frame = ctk.CTkFrame(table_frame)
        header_frame.grid(row=0, column=0, sticky="ew")

        # Add column labels with equal width
        bill_name_header = ctk.CTkLabel(header_frame, text="Bill Name", width=20, anchor="w")
        bill_name_header.grid(row=0, column=0, padx=10, sticky="w")
        amount_header = ctk.CTkLabel(header_frame, text="Amount", width=10, anchor="w")
        amount_header.grid(row=0, column=1, padx=10, sticky="w")
        frequency_header = ctk.CTkLabel(header_frame, text="Frequency", width=15, anchor="w")
        frequency_header.grid(row=0, column=2, padx=10, sticky="w")
        day_header = ctk.CTkLabel(header_frame, text="Day", width=15, anchor="w")
        day_header.grid(row=0, column=3, padx=10, sticky="w")
        start_day_header = ctk.CTkLabel(header_frame, text="Start Date", width=15, anchor="w")
        start_day_header.grid(row=0, column=4, padx=10, sticky="w")
        end_day_header = ctk.CTkLabel(header_frame, text="End Day", width=15, anchor="w")
        end_day_header.grid(row=0, column=5, padx=10, sticky="w")

        # Display each bill in a row
        for i, bill in enumerate(self.bills):
            bill_frame = ctk.CTkFrame(table_frame)
            bill_frame.grid(row=i + 1, column=0, sticky="ew", padx=5, pady=5)

            # Add bill details in the same columns as headers
            bill_name_label = ctk.CTkLabel(bill_frame, text=bill.name, width=20, anchor="w")
            bill_name_label.grid(row=0, column=0, padx=10, sticky="w")
            amount_label = ctk.CTkLabel(bill_frame, text=f"${bill.amount:.2f}", width=10, anchor="w")
            amount_label.grid(row=0, column=1, padx=10, sticky="w")
            frequency_label = ctk.CTkLabel(bill_frame, text=bill.frequency, width=15, anchor="w")
            frequency_label.grid(row=0, column=2, padx=10, sticky="w")
            day_label = ctk.CTkLabel(bill_frame, text=bill.day_of_week, width=15, anchor="w")
            day_label.grid(row=0, column=3, padx=10, sticky="w")

            # If start_date is the current date, display an empty string
            start_date_display = "" if bill.start_date == date.today() else bill.start_date
            start_day_label = ctk.CTkLabel(bill_frame, text=start_date_display, width=15, anchor="w")
            start_day_label.grid(row=0, column=4, padx=10, sticky="w")

            # If end_date is None, display an empty string
            end_day_label = ctk.CTkLabel(bill_frame, text=bill.end_date if bill.end_date else "", width=15, anchor="w")
            end_day_label.grid(row=0, column=5, padx=10, sticky="w")



