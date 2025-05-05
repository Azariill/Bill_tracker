import json
from datetime import date
from models.bill import RecurringBill


def test_recurring_bill_serialization():
    # Step 1: Create a RecurringBill object
    bill = RecurringBill(
        name="Electricity Bill",
        amount=150.0,
        frequency="monthly",
        day_of_week="Monday",
        start_date=date(2025, 5, 1),
        end_date=None
    )

    # Step 2: Convert the RecurringBill object to a dictionary
    bill_dict = bill.to_dict()

    # Step 3: Simulate saving the dictionary to a JSON file (using json.dumps to simulate this)
    json_data = json.dumps(bill_dict, indent=4)
    print("Serialized Bill (JSON format):")
    print(json_data)

    # Step 4: Simulate loading the dictionary from a JSON file (using json.loads)
    loaded_data = json.loads(json_data)

    # Step 5: Recreate the RecurringBill object from the loaded dictionary
    recreated_bill = RecurringBill.from_dict(loaded_data)

    # Step 6: Verify that the original bill and the recreated bill are the same
    print("\nOriginal Bill:")
    print(bill)
    print("\nRecreated Bill:")
    print(recreated_bill)

    # Check if the two objects are the same (by comparing relevant fields)
    if (bill.name == recreated_bill.name and
            bill.amount == recreated_bill.amount and
            bill.frequency == recreated_bill.frequency and
            bill.day_of_week == recreated_bill.day_of_week and
            bill.start_date == recreated_bill.start_date and
            bill.end_date == recreated_bill.end_date):
        print("\nTest Passed: The original and recreated bills match!")
    else:
        print("\nTest Failed: The original and recreated bills do not match.")


if __name__ == "__main__":
    test_recurring_bill_serialization()
