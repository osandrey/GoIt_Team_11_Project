from colorit import *
from prettytable import PrettyTable

def pers_assistant_help():
    pah_com_list = {"tel_book":"TELEPHONE BOOK", "note_book": "NOTE BOOK", "sorted": "SORTED"}
    all_commands = {
        "1":[
            ["show all", "This command show all contacts in your address book", "show all"],
            ["add user", "This command add new user in your address book", "add user <FirstName_LastName> <phone>"],
            ["add phone", "This command add new phone number for existing contact", "add phone <user> <phone>"],
            ["add email", "This command add email for existing contact", "add email <user> <email>"],
            ["add birthday", "This command add birthday for existing contact", "add birthday <user> <date>"],
            ["add adress", "This command add address for existing contact", "add adress <user> <address>"],
            ["change adress", "This command change address for existing contact", "change adress <user> <new_address>"],
            ["change email", "This command change email address for existing contact", "change email <user> <new_email>"],
            ["change birthday", "This command change birthday for existing contact", "change birthday <user> <newBirthday>"],
            ["find name", "This command find all existing contacts whose names match the search query", "find name <name>"],
            ["find phone", "This command find existing contacts whose phone match the search query", "find phone <phone>"],
            ["remove phone", "This command remove phone number for existing contact", "remove phone <user> <phone>"],
            ["remove birthday", "This command remove birthday for existing contact", "remove birthday <user>"],
            ["remove email", "This command remove email address for existing contact", "remove email <user> <email>"],
            ["remove user", "This command remove existing contact and all information about it", "remove user <user>"],
            ["remove adress", "This command remove existing contact and all information about it", "remove adress <user> <address>"],
            ["when birthday", "This command show birthday of existing contact", "when birthday <user>"]
        ],
        "2":[
            ["add or add_note", "This command add new note in your Notepad", "add(add_note) <title> <body> <tags>"],
            ["edit or edit_note", "This command change existing note in your Notepad", "edit(edit_note) <title>"],
            ["delete", "This command delete existing note in your Notepad", "delete <title>"],
            ["find_tags", "This command find existing notes whose tags match the search query", "find_tags <tag>"],
            ["find", "This command find existing notes whose note(body) match the search query", "find <frase>"],
            ["show or show_note", "This command show existing note in your Notepad", "show(show_note) <title>"],
            ["showall", "This command show all existing notes in your Notepad", "showall"],
        ],
        "3": [[
            "sort directory", "This command sort all files in the given directory", "sort directory <path to folder>"
        ]]}
    print(f'''I'm your personal assistant.
I have {pah_com_list['tel_book']}, {pah_com_list['note_book']} and I can {pah_com_list['sorted']} your files in your folder.\n''')
    while True:
        print(f'''If you want to know how to work with:
        "{pah_com_list['tel_book']}" press '1'
        "{pah_com_list['note_book']}" press '2'
        function "{pah_com_list['sorted']}" press '3'
        SEE all comands press '4'
        EXIT from HELP press any other key''')
        user_input = input()
        if user_input not in ["1", "2", "3", "4"]:
            break
        elif user_input in ["1", "2", "3"]:
            my_table = PrettyTable(["Command Name", "Subscribe", "Example"])
            [my_table.add_row(i) for i in all_commands[user_input]]
            my_table.add_row(["quit, close, goodbye, exit", "This command finish work with your assistant", "quit(close, goodbye, exit)"])
            print(my_table)
        else:
            my_table = PrettyTable(["Command Name", "Subscribe", "Example"])
            all_commands_list = sorted([i for j in list(all_commands.values()) for i in j])
            [my_table.add_row(i) for i in all_commands_list]
            my_table.add_row(["quit, close, goodbye, exit", "This command finish work with your assistant", "quit(close, goodbye, exit)"])
            print(my_table)


