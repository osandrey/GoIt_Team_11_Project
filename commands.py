from address_book_classes import contacts_dict, Record, Error
from colorit import *
colorit.init_colorit()
import re


def input_error(function): #Перенис сюди декоратор тут йому буде краще
    """
    Створюємо декоратор для обробки помилок, котрі можуть виникнути через
    ввід користувача.
    :param function: Функція вводу від користувача.
    :return: Або роботу функції або текст з помилкою, для повторного вводу.
    """

    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except KeyError:
            return 'Wrong name'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'Pls print: name and number'
        except TypeError:
            return 'Wrong command.'

    return wrapper


def verify(number):  #перевирка номеру телефона
        number = re.sub(r"[\-\(\)\+\ a-zA-Zа-яА-я]", "", number)
        try:
            if len(number) == 12:
                number = "+" + number
            elif len(number) == 10:
                number = "+38" + number
            elif len(number) == 9:
                number = "+380" + number
            else:
                number = False
                raise Error
        except Error:
            print(color("\nSomething went wrong\n Try again!\n", Colors.green))
        
        if number:
            return number
        else:
            return ""

def verify_date(birth_date: str):
        try:
            birthdate = re.findall(r"\d{4}\.\d{2}\.\d{2}", birth_date)
            if bool(birthdate) == False:
                raise Error
        except Error:
            print(color("\nYou enter wrong date.\nUse this format - YYYY.MM.DD \nTry again!\n", Colors.purple))

        if birthdate:
            return birthdate[0]
        else:
            return ""


@input_error
def hello_func():
    """
    При отриманні команди привіт- маємо зреагувати правильно.
    :return:
    """
    return 'How can I help you?'


@input_error
def exit_func():
    """
    При отриманні слів про вихід з боту- маємо його закрити.
    :return:
    """
    return 'good bye'


@input_error
def add_func(data):
    """
    Додавання нового контакту. Обробка строки и створення контакту. Взаємодія з класами.
    :param data: Строка з ім'ям та телефоном.
    :return: Відповідь, що контакт створено.
    """
    name, phones = create_data(data)

    if name in contacts_dict:
        raise ValueError('This contact already exist.')
    record = Record(name)

    for phone in phones:
        record.add_phone(phone)

    contacts_dict.add_record(record)
    return f'You added new contact: {name} with this {phones}.'


@input_error
def change_phone_func(data):
    """
    Зміна вже існуючого контактного номера. Взаємодія з класами.
    :param data: Строка з ім'ям та телефоном.
    :return: Відповідь про зміни.
    """
    name, phones = create_data(data)
    record = contacts_dict[name]
    record.change_phones(phones)

    return 'Phones were changed.'


@input_error
def search_func(value):
    """
    Коли користувач шукає конкретний контакт за значенням.
    :param value: Контакт котрий шукаємо.
    :return: Повертає дані контакту.
    """
    search_records = ''
    records = contacts_dict.search(value.strip())

    for record in records:
        search_records += f"{record.get_info()}\n"
    return search_records


@input_error
def show_func():
    """
    Показуємо всю книгу контактів створену раніше.
    :return: Список контактів.
    """
    if len(contacts_dict) == 0:
        print("AdressBook is empty")

    contacts = ''
    page_number = 1

    for page in contacts_dict.iterator():
        contacts += f'Page #{page_number}\n'

        for record in page:
            contacts += f'{record.get_info()}\n'
        page_number += 1
    return contacts


@input_error
def del_func(name):
    """
    Функція для видалення контакту за імʼям. Взаємодіє з класами.
    """
    name = name.strip()

    contacts_dict.remove_record(name)
    return "You deleted the contact."


@input_error
def del_phone_func(data):
    name, phone = data.strip().split(' ')

    record = contacts_dict[name]
    if record.delete_phone(phone):
        return f'Phone {phone} for {name} contact deleted.'
    return f'{name} contact does not have this number'


@input_error
def birthday_func(data):
    name, date = data.strip().split(' ')

    record = contacts_dict[name]
    record.add_birthday(date)

    return f'For {name} you add Birthday {date}'


@input_error
def next_birthday_func(name):
    name = name.strip()

    record = contacts_dict[name]

    return f"Days to next birthday of this {name} will be in {record.get_days_to_next_birthday()}."


def create_data(data):
    """
    Розділяє вхідні дані на дві частини - номер і телефон.
    Також ці данні проходять валідацію.
    Для подальшої роботи з ними.
    :param data: Строка з номером і ім'ям.
    :return: Вже розділені ім'я і номер
    """
    name, *phones = data.strip().split(' ')

    if name.isnumeric():
        raise ValueError('Wrong name.')

    return name, phones