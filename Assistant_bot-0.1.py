from collections import UserDict
from datetime import date, datetime


class Field:
    def __init__(self, value=None):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        super().__init__(phone)

    @Field.value.setter
    def value(self, new_value):
        if new_value is not None:
            # Remove non-digit characters from the phone number
            formatted_phone = ''.join(filter(str.isdigit, new_value))
            if len(formatted_phone) == 10:
                self._value = formatted_phone
            else:
                print("Invalid phone number. Please enter a 10-digit phone number.")
        else:
            self._value = None


class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value):
        if new_value is not None:
            try:
                datetime.strptime(new_value, "%Y-%m-%d")
                self._value = new_value
            except ValueError:
                print("Invalid birthday format. Please use the format: YYYY-MM-DD")
        else:
            self._value = None

    def __str__(self):
        if self._value:
            return f"Birthday: {self._value}"
        return ""


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

        if phone is not None:
            self.add_phone(phone)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, index, new_phone):
        if 0 <= index < len(self.phones):
            self.phones[index].value = new_phone

    def delete_phone(self, index):
        if 0 <= index < len(self.phones):
            del self.phones[index]

    def days_to_birthday(self):
        if self.birthday.value is not None:
            today = date.today()
            birthday = datetime.strptime(self.birthday.value, "%Y-%m-%d").date().replace(year=today.year)
            if birthday < today:
                birthday = birthday.replace(year=today.year + 1)
            days_left = (birthday - today).days
            return days_left
        return None

    def birthday_str(self):
        if self.birthday.value:
            return f"Birthday: {self.birthday.value}"
        return ""

    def __str__(self):
        phones = "\n".join(str(phone) for phone in self.phones)
        return f"Name: {self.name}\nPhones:\n{phones}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, n=1):
        items = list(self.data.values())
        for i in range(0, len(items), n):
            yield items[i:i+n]

    def __str__(self):
        records = "\n".join(str(record) for record in self.data.values())
        return f"Address Book:\n{records}"


def hello():
    print("How can I help you?")


def add(name, phone, birthday=None):
    phone_number = phone.replace(" ", "")
    name = name.strip()
    record = Record(name, phone, birthday)
    address_book.add_record(record)
    print(f"{name}'s phone number ({phone_number[-10:]}) has been added to contacts.")


def change(name, phone):
    if name in address_book.data:
        record = address_book.data[name]
        record.edit_phone(0, phone)
        print(f"{name}'s phone number has been updated to {phone}.")
    else:
        print(f"{name} is not in contacts.")


def delete(name):
    if name in address_book.data:
        del address_book.data[name]
        print(f"{name} has been deleted from contacts.")
    else:
        print(f"{name} is not in contacts.")


def phone(name):
    if name in address_book.data:
        record = address_book.data[name]
        print(f"{record.name}:")
        for phone in record.phones:
            print(phone)
    else:
        print(f"{name} is not in contacts.")


def show_all():
    if address_book.data:
        today = date.today()
        for record in address_book.data.values():
            print(f"Name: {record.name}")
            print("\n".join(str(phone) for phone in record.phones))
            print(f"Birthday: {record.birthday}")
            if record.birthday.value:
                days_left = record.days_to_birthday()
                if days_left is not None:
                    print(f"Days until birthday: {days_left}")
            print()
    else:
        print("No contacts to show.")


def exit_program():
    print("Goodbye!")
    quit()


def parse_command(command):
    command = command.strip()
    parts = command.split(' ', 1)
    if parts[0].lower() == 'hello':
        hello()
    elif parts[0].lower() == 'add':
        params = parts[1].split(' ', 2)
        if len(params) == 3:
            add(params[0], params[1], params[2])
        else:
            print("Invalid command: add requires a name, phone number, and birthday.")
    elif parts[0].lower() == 'change':
        params = parts[1].split(' ', 1)
        if len(params) == 2:
            change(params[0], params[1])
        else:
            print("Invalid command: change requires a name and phone number.")
    elif parts[0].lower() == 'delete':
        delete(parts[1])
    elif parts[0].lower() == 'phone':
        phone(parts[1])
    elif parts[0].lower() == 'show' and parts[1].lower() == 'all':
        show_all()
    elif any(word in parts for word in ['goodbye', 'good', 'bye', 'close', 'exit']):
        exit_program()
    else:
        print(f"Invalid command: {command}")


def main():
    global address_book
    address_book = AddressBook()
    while True:
        command = input("Enter command: ")
        parse_command(command.strip())


if __name__ == '__main__':
    main()