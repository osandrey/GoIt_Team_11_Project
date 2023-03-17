from utils import change_input, greeting
from address_book_classes import contacts_dict
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import yes_no_dialog
from colorit import *
colorit.init_colorit()

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
    "delete user",
    "add birthday",
    "days to birthday"

])


def main():
    print(color(greeting,Colors.green))
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

            if user_input in [".", "bye", "good bye", "close", "exit", "bruh"]:
                exit = yes_no_dialog(
                    title='Yes/No dialog example',
                    text='Do you want to close bot?').run()
                if exit:
                    print(color("Bye,see tou soon...",Colors.yellow))
                    break
                else:
                    continue


            if (len(user_input.split())) == 1:
                print(color("Please write full command", Colors.red))
                continue    

            result = change_input(user_input)
            print(result)

    finally:
        contacts_dict.save_contacts_to_file()


if __name__ == '__main__':
    main()