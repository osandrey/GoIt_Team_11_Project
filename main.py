from utils import change_input
from address_book_classes import contacts_dict
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import yes_no_dialog

word_completer = WordCompleter([
    "hello",
    "exit",
    "close",
    "good bye",
    "add",
    "change phone",
    "show all",
    "phone",
    "delete phone",
    "delete",
    "birthday",
    "days to birthday"

])

def main():
    """
    Отримуємо ввід від користувача
    і відправляємо його в середину застосунку на обробку.
    :return:
    """
    try:
        while True:
            """
            Просимо користувача ввести команду для нашого бота
            Також тут же вимикаємо бота якщо було введено відповідну команду
            """
            user_input = prompt('Enter your command: ', completer=word_completer)
            print(user_input)
            if user_input in [".", "bye", "good bye", "close", "exit", "bruh"]:
                exit = yes_no_dialog(
                    title='Yes/No dialog example',
                    text='Do you want to confirm?').run()
                if exit:
                    print("Bye,see tou soon...")
                    break
                else:
                    continue
                
            result = change_input(user_input)
            print(result)
    finally:
        contacts_dict.save_contacts_to_file()


if __name__ == '__main__':
    main()