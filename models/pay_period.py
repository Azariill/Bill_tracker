from datetime import date, timedelta
from typing import List, Optional


class RecurringPayPeriod:
    def __init__(self, name: str, amount: float, frequency: str, day_of_week: str, start_date: date):
        self.name = name
        self.amount = amount
        self.frequency = frequency.lower()
        self.day_of_week = day_of_week.capitalize()
        self.start_date = start_date  # No alignment needed at this point

    def get_weekday_index(self) -> int:
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return weekdays.index(self.day_of_week)

    def _align_to_weekday(self, d: date) -> date:
        """
        Adjust the given date to the next occurrence of the target weekday.
        """
        target_weekday = self.get_weekday_index()
        days_ahead = (target_weekday - d.weekday()) % 7
        return d + timedelta(days=days_ahead)

    def _add_month(self, d: date) -> date:
        month = d.month + 1
        year = d.year
        if month > 12:
            month = 1
            year += 1

        day = min(d.day, [31,
                          29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
                          31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
        return date(year, month, day)

    def get_occurrences_between(self, start_date: date, end_date: date) -> List[date]:
        occurrences = []
        current = self.start_date

        # Fast forward to first occurrence >= start_date
        while current < start_date:
            if self.frequency == "weekly":
                current += timedelta(weeks=1)
            elif self.frequency == "biweekly":
                current += timedelta(weeks=2)
            elif self.frequency == "monthly":
                current = self._add_month(current)
            else:
                return []

        # Collect occurrences in range
        while current <= end_date:
            occurrences.append(current)

            if self.frequency == "weekly":
                current += timedelta(weeks=1)
            elif self.frequency == "biweekly":
                current += timedelta(weeks=2)
            elif self.frequency == "monthly":
                current = self._add_month(current)
            else:
                break

        return occurrences

    def get_pay_date_this_week(self, reference_date: date) -> Optional[date]:
        start_of_week = reference_date - timedelta(days=reference_date.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday
        pay_dates = self.get_occurrences_between(start_of_week, end_of_week)
        return pay_dates[0] if pay_dates else None


# === TESTS ===
if __name__ == "__main__":
    today = date(2025, 5, 9)

    print("========================================")
    print(f"Testing summary for: {today.strftime('%A, %B %d, %Y')}")
    print("========================================\n")

    test_cases = [
        RecurringPayPeriod("Biweekly Pay", 1000.0, "biweekly", "Friday", date(2025, 1, 10)),
        RecurringPayPeriod("Weekly Pay", 500.0, "weekly", "Friday", date(2025, 4, 18)),  # Adjusted to Friday
        RecurringPayPeriod("Monthly Pay", 2000.0, "monthly", "Friday", date(2025, 1, 31))
    ]

    for pay in test_cases:
        print(f"Testing: {pay.name}")
        occurrences = pay.get_occurrences_between(date(2025, 5, 1), date(2025, 5, 15))
        print("  Occurrences between May 1 and May 15:")
        for d in occurrences:
            print(f"    {d.strftime('%A %B %d, %Y')}")

        # Debugging print: Check if the desired date (today) is found
        if today in occurrences:
            print(f"  ✅ {today.strftime('%B %d')} is a valid pay date.")
        else:
            print(f"  ❌ {today.strftime('%B %d')} NOT found in occurrences.")
        print()
