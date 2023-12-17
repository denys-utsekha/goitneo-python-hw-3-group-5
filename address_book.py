from collections import UserDict
from datetime import datetime
import re
from get_birthdays import get_birthdays
import calendar
import pickle


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        self.name = name

    def __is_valid(self, name: str) -> bool:
        return True if name and re.match(r"\b[a-zA-Z]{2,}+\b", name) else False

    @property
    def name(self):
        return self

    @name.setter
    def name(self, name: str):
        if self.__is_valid(name):
            super().__init__(name)
        else:
            raise ValueError(f"{name} is invalid name")


class Phone(Field):
    def __init__(self, phone):
        self.phone = phone

    def __is_valid(self, phone: str) -> bool:
        return True if phone and re.match(r"^\s*(?:[0-9]{10})\s*$", phone) else False

    @property
    def phone(self):
        return self

    @phone.setter
    def phone(self, phone: str):
        if self.__is_valid(phone):
            super().__init__(phone)
        else:
            raise ValueError(f"{phone} is invalid phone")


class Birthday(Field):
    def __init__(self, date):
        self.date = date

    def __is_valid(self, date: str) -> bool:
        return (
            True
            if date and re.match(r"^(\d{1,2})[.](\d{1,2})[.](\d{4})$", date)
            else False
        )

    @property
    def date(self):
        return self

    @date.setter
    def date(self, date: str):
        if self.__is_valid(date):
            splitted = date.split(".")
            try:
                super().__init__(
                    datetime(
                        day=int(splitted[0]),
                        month=int(splitted[1]),
                        year=int(splitted[2]),
                    )
                )
            except:
                raise ValueError(f"{date} is invalid date")
        else:
            raise ValueError(f"{date} is invalid date")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.birthday = None
        self.phone = None

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def add_phone(self, phone):
        self.phone = Phone(phone)

    def __str__(self):
        return (
            f"Contact name: {self.name}, phone: {self.phone}, birthday: {self.birthday}"
        )


class AddressBook(UserDict):
    def add_record(self, name, phone):
        if name in self.data:
            raise KeyError(f"The contact with this name '{name}' already exists.")
        record = Record(name)
        record.add_phone(phone)
        self.data[name] = record

    def find(self, name):
        if not name in self.data:
            raise KeyError(f"The contact with this name '{name}' does not exist.")
        return self.data[name]

    def save_to_file(self):
        with open("address_book.bin", "wb") as file:
            pickle.dump(self, file)

    def read_from_file(self):
        try:
            with open("address_book.bin", "rb") as file:
                return pickle.load(file)
        except:
            return None

    def get_birthdays_per_week(self):
        users = []
        for name in self.keys():
            if self[name].birthday != None:
                users.append({"name": name, "birthday": self[name].birthday.value})

        if len(users) == 0:
            raise ValueError(f"No birthdays were found.")

        birthdays = get_birthdays(users)

        if len(birthdays) == 0:
            raise ValueError(f"No birthdays for next week.")

        result = ""
        for day in sorted(birthdays):
            result += f"{calendar.day_name[day]}: {", ".join(birthdays[day])}\n"
        return result[:-1]
