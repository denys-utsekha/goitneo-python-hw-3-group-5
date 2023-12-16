from book import AddressBook, Record
from get_birthdays import get_birthdays_per_week


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def add_contact(args, book):
    name, phone = args
    new_contact = Record(name)
    new_contact.add_phone(phone)
    new_record = book.add_record(new_contact)
    if new_record:
        return "Contact added."


def change_contact(args, book):
    name, phone = args
    contact = book.find(name)
    if contact:
        contact.add_phone(phone)
        return "Contact changed."


def get_contact_phone(args, book):
    name = args[0]
    contact = book.find(name)
    if contact:
        return book.find(name).phone


def get_all_contacts(book):
    result = ""
    for name in book.keys():
        result += f"{name}: {book[name].phone}\n"
    if len(result) > 0:
        return result[0:-1]
    return "The contact list is empty"


def add_birthday(args, book):
    name, date = args
    contact = book.find(name)
    contact.add_birthday(date)
    return "Birthday added."


def show_birthday(args, book):
    name = args[0]
    if not book.find(name) or book.find(name).birthday == None:
        return "Birthday is not defined"
    birthday = book.find(name).birthday.value
    return f"{birthday.day}.{birthday.month}.{birthday.year}"


def get_birthdays(book):
    data = []
    for name in book.keys():
        data.append({"name": name, "birthday": book[name].birthday.value})
    get_birthdays_per_week(data)


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(get_contact_phone(args, book))
        elif command == "all":
            print(get_all_contacts(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(get_birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
