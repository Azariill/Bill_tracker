import os
import json
from models.bill import RecurringBill
from models.pay_period import RecurringPayPeriod

# Default file paths
BILLS_FILE = '../data/bills.json'
PAY_PERIODS_FILE = '../data/pay_periods.json'


def save_bills(bills, file_path=BILLS_FILE):
    """
    Saves a list of RecurringBill objects to a JSON file.

    :param bills: List of RecurringBill instances
    :param file_path: Path to save the JSON file
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w') as bill_file:
        bills_data = [bill.to_dict() for bill in bills]
        json.dump(bills_data, bill_file, indent=4)


def load_bills(file_path=BILLS_FILE):
    """
    Loads RecurringBill objects from a JSON file.

    :param file_path: Path to the JSON file
    :return: List of RecurringBill instances
    """
    try:
        with open(file_path, 'r') as bill_file:
            bills_data = json.load(bill_file)
            return [RecurringBill.from_dict(bill) for bill in bills_data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_pay_periods(paychecks, file_path=PAY_PERIODS_FILE):
    """
    Saves a list of RecurringPayPeriod objects to a JSON file.

    :param paychecks: List of RecurringPayPeriod instances
    :param file_path: Path to save the JSON file
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w') as pay_file:
        paychecks_data = [paycheck.to_dict() for paycheck in paychecks]
        json.dump(paychecks_data, pay_file, indent=4)


def load_pay_periods(file_path=PAY_PERIODS_FILE):
    """
    Loads RecurringPayPeriod objects from a JSON file.

    :param file_path: Path to the JSON file
    :return: List of RecurringPayPeriod instances
    """
    try:
        with open(file_path, 'r') as pay_file:
            paychecks_data = json.load(pay_file)
            return [RecurringPayPeriod.from_dict(paycheck) for paycheck in paychecks_data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []
