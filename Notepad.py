import functools
import subprocess
import pickle
import re
from collections import UserDict
from typing import Callable
from colorit import *
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

colorit.init_colorit()

class MyException(Exception):
    pass

class Notepad(UserDict):

    def __getitem__(self, title):
        if not title in self.data.keys():
            raise MyException(color("This article isn't in the Notepad",Colors.red))
        note = self.data[title]
        return note
    
    def add_note(self, note) -> str:
        self.data.update({note.title.value:note})
        return color('Done!',Colors.blue)

    def delete_note(self, title):
        try:
            self.data.pop(title)
            return color(f"{title} was removed",Colors.purple)
        except KeyError:
            return color("This note isn't in the Notepad",Colors.blue)

    def get_notes(self, file_name):
        with open(file_name, 'ab+') as fh:
            fh.seek(0)
            try:
                self.data = pickle.load(fh)
            except EOFError:
                pass 
         
    def find_note(self):
        pass

    def show_notes_titles(self):
        res =  "\n".join([note for note in notes])
        return color(res,Colors.orange)
    
    def write_notes(self, file_name):
        with open(file_name, "wb") as fh:
            pickle.dump(self, fh)

class Field:

    def __init__(self, value):
        self.__value = None
        self.value = value

class NoteTag(Field):
    pass

class NoteTitle(Field):

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, title):
        if len(title) == 0:
            raise ValueError(color("The title wasn't added. It should have at least 1 character.",Colors.red))
        self.__value = title

class NoteBody(Field):
    pass

class Note:
    
    def __init__(self, title: NoteTitle, body: NoteBody, tags: list[NoteTag]=None) -> None:
        self.title = title
        self.body = body if body else ''
        self.tags = tags if tags else ''

    def edit_tags(self, tags: list[NoteTag]):
        self.tags = tags

    def edit_title(self, title: NoteTitle):
        self.title = title

    def edit_body(self, body: NoteBody):
        self.body = body

    def show_note(self):
        return '\n'.join([f"Title: {self.title.value}", f"Body: {self.body.value}", f"Tags: {self.show_tags()}"])
    
    def show_tags(self):
        if self.tags == []:
            return "Tags: Empty",Colors.red
        return ', '.join([tag.value for tag in self.tags])
        
def decorator_input(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*words):
        try:
            return func(*words)
        except KeyError as err:
            return err
        except IndexError:
            return color("You didn't enter the title or keywords",Colors.red)
        except TypeError:
            return color("Sorry, this command doesn't exist",Colors.red)
        except Exception as err:
            return err
    return wrapper

@decorator_input
def add_note(*args) -> str:
    title = NoteTitle(input(color("Enter the title: ",Colors.yellow)))
    if title.value in notes.data.keys():
        raise MyException(color('This title already exists',Colors.red))
    body = NoteBody(input(color("Enter the note: ",Colors.yellow)))
    tags = input(color("Enter tags (separate them with ',') or press Enter to skip this step: ",Colors.yellow))
    tags = [NoteTag(t.strip()) for t in tags.split(',')]
    note = Note(title, body, tags)
    return notes.add_note(note)


@decorator_input
def delete_note(*args: str) -> str:
    return notes.delete_note(args[0])

@decorator_input        
def edit_note(*args) -> str:
    title = args[0]
    if title in notes.data.keys():
        note = notes.data.get(title)
    user_title = input(color("Enter new title or press 'enter' to skip this step: ",Colors.yellow))
    if user_title:
        if not user_title in notes.data.keys():
            notes.data[user_title] = notes.data.pop(title)
            note.edit_title(NoteTitle(user_title))
        else:
            raise MyException(color('This title already exists.',Colors.red))
    try:
        body = edit(note.body.value, 'body')
        if body:
            body = NoteBody(body)
            note.edit_body(body)
    except Exception as err:
        print(err)

    try:
        tags = edit(note.show_tags(), 'tags')
        if tags:
            tags = [NoteTag(t.strip()) for t in tags.split(',')]
            note.edit_tags(tags)
    except Exception as err: 
        print(err)

    return "Done!"
    
@decorator_input
def goodbye() -> str:
    return 'Goodbye!'

@decorator_input
def show_note(*args:str) -> str:
    note = notes.data.get(args[0])
    return note.show_note()

@decorator_input
def edit(text: str, part) -> str:
    user_input = input(color(f"Enter any letter if you want to edit {part} or press 'enter' to skip this step. ",Colors.green))
    if user_input:
        with open('edit_note.txt', 'w') as fh:
            fh.write(text)
        subprocess.Popen(['open', 'edit_note.txt'])
        mes = ''
        if part == 'tags':
            mes = color("Separate tags with ','",Colors.green)
        input(color(f'Press enter or any letter if you finished editing. Please, make sure you closed the text editor. {mes}',Colors.green))
        with open('edit_note.txt', 'r') as fh:
            edited_text = fh.read()
        return edited_text
    
def find(*args) -> str:
    try:
        re.match(r'^\s*$', args)
    except TypeError:
        args = input(color("Enter the phrase you want to find: ",Colors.yellow))
    notes_list = []
    for note in notes.data.values():
        if re.search(args, note.body.value) or re.search(args, note.title.value, flags=re.IGNORECASE):
            notes_list.append(note.title.value)
    if len(notes_list) == 0:
        return "No matches"
    return '\n'.join([title for title in notes_list])
    
@decorator_input  
def find_tags(*args: str) -> str:
    if len(args) == 0:
        return "You didn't enter any tags."
    all_notes = [note for note in notes.data.values()]
    notes_dict = {title:[] for title in notes.data.keys()}
    for arg in args:
        for note in all_notes:
            if arg in [tag.value for tag in note.tags]:
                notes_dict[note.title.value].append(arg)
    sorted_dict = sorted(notes_dict, key=lambda k: len(notes_dict[k]), reverse=True)
    return '\n'.join([f"{key}:{notes_dict[key]}" for key in sorted_dict if len(notes_dict[key]) > 0])

def get_command(words: str) -> Callable:
    
    if words[0] == '':
        raise KeyError ("This command doesn't exist")
    for key in commands_dict.keys():
        try:
            if re.search(fr'\b{words[0].lower()}\b', str(key)):
                func = commands_dict[key]
                return func
        except (re.error):
            break
    raise KeyError ("This command doesn't exist")

notes = Notepad()
notes.get_notes('notes.bin')

commands_dict = {('add', 'add_note'):add_note,
                 ('edit', 'edit_note'):edit_note,
                 ('show', 'show_note'):show_note,
                 ('showall',):notes.show_notes_titles,
                 ('find_tags',):find_tags,
                 ('find',):find,
                 ('delete',):delete_note,
                 ('goodbye','close','exit','quit'):goodbye
}

word_completer = WordCompleter(["add", "add_note", "edit", "edit_note", "show", "show_note", "showall" ,"find_tags", "find", "delete" ,"."])
def main():

    while True:
        words = prompt('Enter your command: ', completer=word_completer).split(" ")
        try:
            func = get_command(words)
        except KeyError as error:
            print(error)
            continue
        print(func(*words[1:])) 
        if func.__name__ == 'goodbye':
            notes.write_notes('notes.bin')
            break

if __name__ == '__main__':
    main()

