import functools
import subprocess
import pickle
import re
from collections import UserDict
from typing import Callable

class MyException(Exception):
    pass

class Notepad(UserDict):
    
    def add_note(self, note) -> str:
        self.data.update({note.title.value:note})
        return 'Done!'

    def delete_note(self, title):
        try:
            self.data.pop(title)
            return f"{title} was removed"
        except KeyError:
            return "This note isn't in the Notepad"

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
        return "\n".join([note for note in notes])
    
    def write_notes(self, file_name):
        with open(file_name, "wb") as fh:
            pickle.dump(self, fh)

class Field:

    def __init__(self, value):
        self.value = value

class NoteTag(Field):
    pass

class NoteTitle(Field):
    pass

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
        return '\n'.join([self.title.value, self.body.value, ', '.join([f"#{tag.value}" for tag in self.tags])])
    
    def show_tags(self):
        if self.tags == []:
            return ""
        return ", ".join([tag.value for tag in self.tags])
                      
        
def decorator_input(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*words):
        try:
            return func(*words)
        except KeyError as err:
            return err
        except IndexError:
            return "You didn't enter the title or keywords"
        except TypeError:
            return "Sorry, this command doesn't exist"
        except Exception as err:
            return err
    return wrapper

@decorator_input
def add_note() -> str:
    title = NoteTitle(input("Enter the title: "))
    if title.value in notes.data.keys():
        raise MyException('This title already exists')
    body = NoteBody(input("Enter the note: "))
    tags = input("Enter tags (separate them with ',') or press Enter to skip this step: ")
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
    user_title = input("Enter new title or press 'enter' to skip this step: ")
    if user_title:
        if not user_title in notes.data.keys():
            note.edit_title(NoteTitle(user_title))
        else:
            raise MyException('This title already exists.')
    
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
def show_note(*args):
    note = notes.data.get(args[0])
    return note.show_note()

@decorator_input
def edit(text: str, part) -> str:
    user_input = input(f"Enter any letter if you want to edit {part} or press 'enter' to skip this step. ")
    if user_input:
        with open('edit_note.txt', 'w') as fh:
            fh.write(text)
        subprocess.Popen(['open', 'edit_note.txt'])
        mes = ''
        if part == 'tags':
            mes = "Separate tags with ','"
        input(f'Press enter or any letter if you finished editing. Please, make sure you closed the text editor. {mes}')
        with open('edit_note.txt', 'r') as fh:
            edited_text = fh.read()
        return edited_text

def get_command(words: str) -> Callable:
    for key in commands_dict.keys():
        try:
            if re.search(fr'\b{words[0].lower()}\b', str(key)):
                func = commands_dict[key]
                return func
        except re.error:
            break
    raise KeyError("This command doesn't exist") 

notes = Notepad()
notes.get_notes('notes.bin')

commands_dict = {('add',): add_note,
                 ('edit'): edit_note,
                 ('show'): show_note,
                 ('showall',): notes.show_notes_titles,
                #  ('find',):find,
                 ('delete',):delete_note,
                 ('goodbye','close','exit','quit'):goodbye
}
    

def main():

    while True:
        words = input(">>> ").split(' ')
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







