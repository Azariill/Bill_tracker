from datetime import date, timedelta
from typing import List, Tuple
from models.bill import RecurringBill
from models.pay_period import RecurringPayPeriod


# Function to get the start and end of the week
def get_week_range(today: date) -> Tuple[date, date]:
    """
    Returns the start (Monday) and end (Sunday) of the week for the given date.
    """
    start_of_week = today - timedelta(days=today.weekday())  # Start of the week (Monday)
    end_of_week = start_of_week + timedelta(days=6)  # End of the week (Sunday)
    return start_of_week, end_of_week

# Function to get bills due and overdue this week
def get_bills_this_week(bills: List[RecurringBill], today: date):
    """
    Returns all bills scheduled this week, and a list of bills that are overdue.
    """
    start, end = get_week_range(today)
    bills_due = []
    overdue = []

    for bill in bills:
        occurrences = bill.get_occurrences_between(start, end)
        for occ in occurrences:
            if occ < today:
                overdue.append((bill, occ))  # If bill due date is before today, it is overdue
            else:
                bills_due.append((bill, occ))  # If bill due date is after today, it is due this week

    return bills_due, overdue

# Function to get paychecks due this week
def get_paychecks_this_week(pay_periods: List[RecurringPayPeriod], today: date):
    """
    Returns all paychecks this week and flags if they are past or upcoming.
    """
    start, end = get_week_range(today)
    occurred = []
    upcoming = []

    for period in pay_periods:
        pay_dates = period.get_occurrences_between(start, end)
        for pd in pay_dates:
            if pd < today:
                occurred.append((period, pd))  # Paycheck that has already occurred
            else:
                upcoming.append((period, pd))  # Paycheck that is upcoming

    return occurred, upcoming

# Global balance and disposable income calculation
def calculate_balance_and_income(paychecks: List[RecurringPayPeriod], bills: List[RecurringBill], today: date):
    """
    Calculates the global balance and estimated disposable income for the week.
    """
    total_income = 0
    total_bills = 0

    # Add income from occurred paychecks
    occurred, _ = get_paychecks_this_week(paychecks, today)
    for pay, _ in occurred:
        total_income += pay.amount

    # Add bills that have occurred this week (or are overdue)
    due_bills, overdue_bills = get_bills_this_week(bills, today)
    for bill, _ in due_bills + overdue_bills:
        total_bills += bill.amount

    disposable_income = total_income - total_bills

    return total_income, total_bills, disposable_income

# Confirm if a bill has been processed if it's overdue
def confirm_bill_payment(bills: List[RecurringBill], today: date):
    """
    Ask the user to confirm if overdue bills have been processed.
    """
    _, overdue_bills = get_bills_this_week(bills, today)
    for bill, date_due in overdue_bills:
        # Show overdue bills and ask for confirmation
        print(f"Bill: {bill.name} due on {date_due.strftime('%A %m/%d')}")
        confirmation = input(f"Has {bill.name} been processed? (y/n): ").lower()
        if confirmation == 'y':
            # Process payment and update balance
            print(f"{bill.name} payment confirmed.")
        else:
            print(f"{bill.name} payment still pending.")

if __name__ == "__main__":
    test_dates = [
        date(2025, 5, 1),   # Thursday
        date(2025, 5, 3),   # Saturday
        date(2025, 5, 5),   # Monday (new week)
        date(2025, 4, 25),  # Previous week
        date(2025, 5, 9),   # Following week (Friday paycheck)
    ]

    # Sample bills and paychecks
    bills = [
        RecurringBill("Phone Bill", 60.0, "monthly", "Wednesday", date(2024, 1, 15)),
        RecurringBill("Car Payment", 300.0, "monthly", "Thursday", date(2024, 2, 15)),
        RecurringBill("Internet", 80.0, "monthly", "Friday", date(2025, 1, 5)),
    ]

    pays = [
        RecurringPayPeriod("Job", 1000.0, "biweekly", "Friday", date(2025, 1, 10)),
        RecurringPayPeriod("Side Gig", 500.0, "monthly", "Monday", date(2025, 1, 6)),
    ]

    for today in test_dates:
        print("=" * 40)
        print(f"Testing summary for: {today.strftime('%A, %B %d, %Y')}")
        print("=" * 40)

        # Get bills due this week and overdue bills
        due, overdue = get_bills_this_week(bills, today)
        print("\nBills Due This Week:")
        if due:
            for bill, date_due in due:
                print(f"  {bill.name} on {date_due.strftime('%A %m/%d')}")
        else:
            print("  None")

        print("\nOverdue Bills:")
        if overdue:
            for bill, date_due in overdue:
                print(f"  {bill.name} was due on {date_due.strftime('%A %m/%d')}")
        else:
            print("  None")

        # Get paychecks occurred this week and upcoming paychecks
        occurred, upcoming = get_paychecks_this_week(pays, today)
        print("\nPay Received:")
        if occurred:
            for pay, pd in occurred:
                print(f"  {pay.name} on {pd.strftime('%A %m/%d')}")
        else:
            print("  None")

        print("\nUpcoming Pay:")
        if upcoming:
            for pay, pd in upcoming:
                print(f"  {pay.name} coming on {pd.strftime('%A %m/%d')}")
        else:
            print("  None")

        # Calculate global balance and disposable income
        total_income, total_bills, disposable_income = calculate_balance_and_income(pays, bills, today)

        print(f"\nTotal Income for the Week: ${total_income}")
        print(f"Total Bills for the Week: ${total_bills}")
        print(f"Estimated Disposable Income: ${disposable_income}")

        print("\n" + "-" * 40 + "\n")

