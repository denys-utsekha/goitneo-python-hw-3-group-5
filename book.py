from collections import UserDict
from datetime import datetime
import re


class PhoneAlreadyExistError(Exception):
    pass


class RecordAlreadyExistError(Exception):
    pass


class RecordNotExistError(Exception):
    pass


class PhoneNotExistError(Exception):
    pass


def handle_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PhoneAlreadyExistError:
            print("Such a phone already exists")
        except PhoneNotExistError:
            print("There is no such phone.")
        except RecordAlreadyExistError:
            print("A record with this name already exists.")
        except RecordNotExistError:
            print("No such record found.")
        except KeyError:
            print("Nothing was found for this key.")

    return inner


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
                        year=int(splitted[2]),
                        day=int(splitted[1]),
                        month=int(splitted[0]),
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

    @handle_error
    def add_birthday(self, date):
        self.birthday = Birthday(date)

    @handle_error
    def add_phone(self, phone):
        self.phone = Phone(phone)

    def __str__(self):
        return (
            f"Contact name: {self.name}, phone: {self.phone}, birthday: {self.birthday}"
        )


class AddressBook(UserDict):
    @handle_error
    def add_record(self, record):
        if record.name.value in self.data:
            raise RecordAlreadyExistError
        self.data[record.name.value] = record
        return self.data[record.name.value]

    @handle_error
    def find(self, name):
        if not self.data[name]:
            raise RecordNotExistError
        return self.data[name]
