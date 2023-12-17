from address_book import AddressBook, Record


def handle_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return e
        except KeyError as e:
            return e

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@handle_error
def add_contact(args, book):
    name, phone = args
    book.add_record(name, phone)
    return "Contact added."


@handle_error
def change_contact(args, book):
    name, phone = args
    book.find(name).add_phone(phone)
    return "Contact changed."


@handle_error
def get_contact_phone(args, book):
    name = args[0]
    return book.find(name).phone


@handle_error
def get_all_contacts(book):
    result = ""
    for name in book.keys():
        result += f"{name}: {book[name].phone}\n"
    if len(result) > 0:
        return result[0:-1]
    return "The contact list is empty"


@handle_error
def add_birthday(args, book):
    name, date = args
    contact = book.find(name)
    contact.add_birthday(date)
    return "Birthday added."


@handle_error
def show_birthday(args, book):
    name = args[0]
    contact = book.find(name)
    if contact.birthday == None:
        raise ValueError(f"'{name}' birthday is not defined")
    birthday = contact.birthday.value
    return f"{birthday.day}.{birthday.month}.{birthday.year}"


@handle_error
def get_birthdays(book):
    print(book.get_birthdays_per_week())


def main():
    new_address_book = AddressBook()
    restore_address_book = new_address_book.read_from_file()
    address_book = (
        restore_address_book if restore_address_book != None else new_address_book
    )

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            address_book.save_to_file()
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, address_book))
        elif command == "change":
            print(change_contact(args, address_book))
        elif command == "phone":
            print(get_contact_phone(args, address_book))
        elif command == "all":
            print(get_all_contacts(address_book))
        elif command == "add-birthday":
            print(add_birthday(args, address_book))
        elif command == "show-birthday":
            print(show_birthday(args, address_book))
        elif command == "birthdays":
            print(get_birthdays(address_book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
