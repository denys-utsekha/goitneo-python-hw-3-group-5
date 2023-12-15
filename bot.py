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
    book.add_record(new_contact)
    return "Contact added."


def add_birthday(args, book):
    name, date = args
    contact = book.find(name)
    contact.add_birthday(date)
    return "Birthday added."


def change_contact(args, book):
    name, phone = args
    contact = book.find(name)
    contact.edit_phone(contact.phones[0], phone)
    return "Contact changed."


def get_contact_phone(args, book):
    name = args[0]
    return book.find(name).phones[0]


def get_all_contacts(book):
    result = ""
    for name in book.keys():
        result += f"{name}: {book[name].phones[0]}\n"
    return result[0:-1]


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
        elif command == "birthdays":
            print(get_birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()