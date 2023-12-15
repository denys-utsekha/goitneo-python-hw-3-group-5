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
            super().__init__(None)
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
            super().__init__(None)
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
            super().__init__(
                datetime(
                    year=int(splitted[2]), day=int(splitted[1]), month=int(splitted[0])
                )
            )
        else:
            super().__init__(None)
            raise ValueError(f"{date} is invalid date")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.birthday = None
        self.phones = []

    @handle_error
    def add_birthday(self, date):
        self.birthday = Birthday(date)

    @handle_error
    def add_phone(self, phone):
        if self.find_phone(phone):
            raise PhoneAlreadyExistError
        self.phones.append(Phone(phone))

    @handle_error
    def remove_phone(self, phone):
        if not self.find_phone(phone):
            raise PhoneNotExistError
        self.phones = list(
            filter(lambda current_phone: current_phone.value != phone, self.phones)
        )

    @handle_error
    def edit_phone(self, old_phone, new_phone):
        if not self.find_phone(old_phone):
            raise PhoneNotExistError
        self.phones = list(
            map(
                lambda current_phone: current_phone
                if current_phone.value != old_phone
                else Phone(new_phone),
                self.phones,
            )
        )

    def find_phone(self, search_phone):
        result = list(filter(lambda phone: phone.value == search_phone, self.phones))
        return result[0] if len(result) else None

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"


class AddressBook(UserDict):
    @handle_error
    def add_record(self, record):
        if record.name.value in self.data:
            raise RecordAlreadyExistError
        self.data[record.name.value] = record

    @handle_error
    def find(self, name):
        return self.data[name]

    @handle_error
    def delete(self, name):
        del self.data[name]
