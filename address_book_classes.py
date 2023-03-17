import pickle
from datetime import datetime
from collections import UserDict
from colorit import *
colorit.init_colorit()

class Error(Exception):
    pass



class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, value):
        if len(value) < 10 or len(value) > 12:
            raise ValueError("Phone must contains 10 symbols.")
        if not value.isnumeric():
            raise ValueError('Wrong phones.')
        self._value = value


class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        today = datetime.now().date()
        birth_date = datetime.strptime(value, '%Y.%m.%d').date()
        if birth_date > today:
            raise ValueError("Birthday must be less than current year and date.")
        self._value = value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def get_info(self):
        phones_info = ''
        birthday_info = ''

        for phone in self.phones:
            phones_info += f'{phone.value}, '

        if self.birthday:
            birthday_info = f' Birthday : {self.birthday.value}'

        return f'{self.name.value} : {phones_info[:-2]}{birthday_info}'

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        for record_phone in self.phones:
            if record_phone.value == phone:
                self.phones.remove(record_phone)
                return True
        return False

    def change_phones(self, phones):
        for phone in phones:
            if not self.delete_phone(phone):
                self.add_phone(phone)

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def get_days_to_next_birthday(self):
        if not self.birthday:
            raise ValueError("This contact doesn't have attribute birthday")

        today = datetime.now().date()
        birthday = datetime.strptime(self.birthday.value, '%Y-%m-%d').date()

        next_birthday_year = today.year

        if today.month >= birthday.month and today.day > birthday.day:
            next_birthday_year += 1

        next_birthday = datetime(
            year=next_birthday_year,
            month=birthday.month,
            day=birthday.day
        )

        return (next_birthday.date() - today).days


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

        self.load_contacts_from_file()

    def add_record(self, record):
        self.data[record.name.value] = record

    def get_all_record(self):
        return self.data

    def has_record(self, name):
        return bool(self.data.get(name))

    def get_record(self, name) -> Record:
        return self.data.get(name)

    def remove_record(self, name):
        del self.data[name]

    def search(self, value):
        record_result = []
        for record in self.get_all_record().values():
            if value in record.name.value:
                record_result.append(record)
                continue

            for phone in record.phones:
                if value in phone.value:
                    record_result.append(record)

        if not record_result:
            raise ValueError("Contacts with this value does not exist.")
        return record_result

    def iterator(self, count=5):
        page = []
        i = 0

        for record in self.data.values():
            page.append(record)
            i += 1

            if i == count:
                yield page
                page = []
                i = 0

        if page:
            yield page

    def save_contacts_to_file(self):
        with open('address_book.pickle', 'wb') as file:
            pickle.dump(self.data, file)

    def load_contacts_from_file(self):
        try:
            with open('address_book.pickle', 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            pass


contacts_dict = AddressBook()