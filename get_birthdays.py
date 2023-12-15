from datetime import datetime
from collections import defaultdict
from enum import Enum
import calendar


class Weekdays(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


PERIOD = 7


def get_birthdays_per_week(users):
    result = defaultdict(list)
    today = datetime.today().date()
    print(f"tye - {type(users)}")
    print(f"users - {users}")
    for user in users:
        print(f"user - {user}")
        name = user["name"]
        birthday = user["birthday"].date()
        birthday_this_year = birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday.replace(year=today.year + 1)

        delta_days = (birthday_this_year - today).days

        if delta_days < PERIOD:
            birthday_weekday = birthday_this_year.weekday()
            today_weekday = today.weekday()

            if birthday_weekday in [Weekdays.SATURDAY.value, Weekdays.SUNDAY.value]:
                if not today_weekday in [
                    Weekdays.MONDAY.value,
                    Weekdays.SUNDAY.value,
                ] or (
                    today_weekday == Weekdays.SUNDAY.value
                    and birthday_weekday == Weekdays.SUNDAY.value
                ):
                    result[Weekdays.MONDAY.value].append(name)
            else:
                result[birthday_weekday].append(name)

    for day in sorted(result):
        print(f"{calendar.day_name[day]}: {", ".join(result[day])}")
