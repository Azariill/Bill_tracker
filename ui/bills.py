import customtkinter as ctk
from tkcalendar import DateEntry
import datetime


class BillsPage(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.pack(fill="both", expand=True)

        self.create_widgets()

    def create_widgets(self):
        # Form variables
        self.bill_name_var = ctk.StringVar()
        self.bill_amount_var = ctk.StringVar()
        self.bill_frequency_var = ctk.StringVar()
        self.bill_day_var = ctk.StringVar()
        self.bill_start_date_var = ctk.StringVar()
        self.bill_end_date_var = ctk.StringVar()

        # Section Label
        add_bill_label = ctk.CTkLabel(
            self, text="Add New Bill", font=ctk.CTkFont(size=10, weight="bold")
        )
        add_bill_label.pack(pady=(10, 5))

        # Bill Name
        create_entry_label_frame(self, "Bill Name", self.bill_name_var)

        # Amount
        create_entry_label_frame(self, "Amount", self.bill_amount_var)

        # Frequency
        create_entry_label_frame(
            self, "Frequency (weekly, biweekly, monthly)", self.bill_frequency_var
        )

        # Day of week
        ctk.CTkLabel(self, text="Day of Week").pack(pady=(5, 0))
        self.bill_day_var.set("Monday")
        ctk.CTkOptionMenu(
            self,
            values=[
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ],
            variable=self.bill_day_var,
        ).pack(pady=(0, 5))

        # Start Date
        ctk.CTkLabel(self, text="Start Date").pack()
        self.start_date_picker = DateEntry(
            self, textvariable=self.bill_start_date_var, date_pattern="yyyy-mm-dd"
        )
        self.start_date_picker.pack(pady=2)

        # End Date
        ctk.CTkLabel(self, text="End Date").pack()
        self.end_date_picker = DateEntry(
            self, textvariable=self.bill_end_date_var, date_pattern="yyyy-mm-dd"
        )
        self.end_date_picker.pack(pady=2)

        # Add Bill Button
        create_button(self, "Add Bill", self.add_bill)

        # Bill Display Placeholder
        self.bills_label = ctk.CTkLabel(self, text="Bills will display here.")
        self.bills_label.pack(pady=10)

    def add_bill(self):
        # Example logic (add database or list saving here)
        name = self.bill_name_var.get()
        amount = self.bill_amount_var.get()
        freq = self.bill_frequency_var.get()
        day = self.bill_day_var.get()
        start = self.bill_start_date_var.get()
        end = self.bill_end_date_var.get()

        summary = f"Added Bill: {name}, ${amount}, {freq}, every {day}, {start} - {end}"
        self.bills_label.configure(text=summary)


# --- Widget Helpers ---


def create_entry_label_frame(parent, label_text, variable):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(pady=5)

    label = ctk.CTkLabel(frame, text=label_text)
    label.pack(side="top", anchor="w")

    entry = ctk.CTkEntry(frame, textvariable=variable)
    entry.pack()


def create_button(parent, text, command):
    button = ctk.CTkButton(parent, text=text, command=command)
    button.pack(pady=10)
