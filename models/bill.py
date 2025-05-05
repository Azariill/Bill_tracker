from datetime import date, timedelta
from typing import Optional, List


class RecurringBill:
    """
    Represents a recurring bill (e.g., subscriptions, loans, utilities) that can be tracked
    weekly, biweekly, or monthly. Optionally ends after a fixed date, with calculation for remaining payments.
    """

    def __init__(self, name: str, amount: float, frequency: str, day_of_week: str, start_date: Optional[date],
                 end_date: Optional[date] = None):
        self.name = name
        self.amount = amount
        self.frequency = frequency.lower()
        self.day_of_week = day_of_week.capitalize()
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return f"<RecurringBill {self.name} - ${self.amount:.2f} {self.frequency} on {self.day_of_week}>"

    def to_dict(self):
        """
        Converts the RecurringBill object into a dictionary format for JSON serialization.
        """
        return {
            'name': self.name,
            'amount': self.amount,
            'frequency': self.frequency,
            'day_of_week': self.day_of_week,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a RecurringBill object from a dictionary format.
        """
        start_date = date.fromisoformat(data['start_date']) if data['start_date'] else None
        end_date = date.fromisoformat(data['end_date']) if data['end_date'] else None
        return cls(
            name=data['name'],
            amount=data['amount'],
            frequency=data['frequency'],
            day_of_week=data['day_of_week'],
            start_date=start_date,
            end_date=end_date
        )

    def get_occurrences_between(self, start: date, end: date) -> List[date]:
        """
        Return all dates this bill occurs between `start` and `end`, inclusive.
        """
        occurrences = []
        if end < start:
            return occurrences

        # Determine numeric weekday
        target_weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(
            self.day_of_week)

        # Find the first possible due date >= start
        current = self.start_date
        while current < start:
            current = self._advance(current)

        # Add all valid due dates until end (or end_date)
        while current <= end:
            if self.end_date and current > self.end_date:
                break
            if current.weekday() == target_weekday:
                occurrences.append(current)
            current = self._advance(current)

        return occurrences

    def _advance(self, current: date) -> date:
        """
        Advance to the next due date based on frequency.
        """
        if self.frequency == "weekly":
            return current + timedelta(weeks=1)
        elif self.frequency == "biweekly":
            return current + timedelta(weeks=2)
        elif self.frequency == "monthly":
            # Monthly: add one month while preserving the day as best as possible
            month = current.month + 1
            year = current.year + (month - 1) // 12
            month = (month - 1) % 12 + 1
            day = min(current.day, 28)  # Use 28 to avoid invalid dates like Feb 30
            return date(year, month, day)
        else:
            raise ValueError(f"Unsupported frequency: {self.frequency}")

    def payments_made_by(self, as_of: date) -> int:
        """
        Returns how many times this bill would have occurred on or before a specific date.
        """
        count = 0
        current = self.start_date

        while current <= as_of:
            if self.end_date and current > self.end_date:
                break
            if current.weekday() == ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
                                     "Sunday"].index(self.day_of_week):
                count += 1
            current = self._advance(current)

        return count

    def total_payments(self) -> Optional[int]:
        """
        Return the total number of payments over the full range if end_date is set.
        Otherwise, return None.
        """
        if not self.end_date:
            return None
        return self.payments_made_by(self.end_date)

    def remaining_payments(self, as_of: date) -> Optional[int]:
        """
        Calculate remaining payments, return None if no end date.
        """
        if not self.end_date:
            return None
        total = self.total_payments()
        payments_made = self.payments_made_by(as_of)
        return total - payments_made if total is not None else None

    def payment_status(self, as_of: date) -> str:
        """
        Return a string like 'Payment 3 of 12' or 'Payment 5 of ?' depending on whether end_date is known.
        """
        current_count = self.payments_made_by(as_of)
        total = self.total_payments()
        if total is not None:
            return f"Payment {current_count} of {total}"
        return f"Payment {current_count} of ?"
