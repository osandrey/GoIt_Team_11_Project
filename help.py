from colorit import *
from prettytable import PrettyTable

def pers_assistant_help():
    pah_com_list = {"tel_book":"TELEPHONE BOOK", "note_book": "NOTE BOOK", "sorted": "SORTED"}
    all_commands = {
        "1":[
            ["show all", "This command shows all contacts in your address book", "show all"],
            ["add user", "This command adds a new user in your address book", "add user <FirstName_LastName> <phone>"],
            ["add phone", "This command adds a new phone number for an existing contact", "add phone <user> <phone>"],
            ["add email", "This command adds an email for an existing contact", "add email <user> <email>"],
            ["add birthday", "This command adds a birthday for an existing contact", "add birthday <user> <date>"],
            ["add adress", "This command adds an address for an existing contact", "add adress <user> <address>"],
            ["change adress", "This command changes an address for an existing contact", "change adress <user> <new_address>"],
            ["change email", "This command changes an email address for an existing contact", "change email <user> <new_email>"],
            ["change birthday", "This command changes a birthday for an existing contact", "change birthday <user> <newBirthday>"],
            ["find name", "This command finds all existing contacts whose names match the search query", "find name <name>"],
            ["find phone", "This command finds existing contacts whose phone match the search query", "find phone <phone>"],
            ["remove phone", "This command removes a phone number for an existing contact", "remove phone <user> <phone>"],
            ["remove birthday", "This command removes a birthday for an existing contact", "remove birthday <user>"],
            ["remove email", "This command removes an email address for an existing contact", "remove email <user> <email>"],
            ["remove user", "This command removes an existing contact and all the information about it", "remove user <user>"],
            ["remove adress", "This command removes an existing contact and all the information about it", "remove adress <user> <address>"],
            ["when birthday", "This command shows a birthday of an existing contact", "when birthday <user>"]
        ],
        "2":[
            ["add or add_note", "This command adds a new note in your Notepad", "add(add_note) <title> <body> <tags>"],
            ["edit or edit_note", "This command changes an existing note in your Notepad", "edit(edit_note) <title>"],
            ["delete", "This command deletes an existing note in your Notepad", "delete <title>"],
            ["find_tags", "This command finds and sorts existing notes whose tags match the search query", "find_tags <tag>"],
            ["find", "This command finds existing notes whose note(body) matches the search query", "find <frase>"],
            ["show or show_note", "This command shows an existing note in your Notepad", "show(show_note) <title>"],
            ["showall", "This command shows all existing notes in your Notepad", "showall"],
        ],
        "3": [[
            "sort directory", "This command sorts all files in the given directory", "sort directory <path to folder>"
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


