import argparse
import os
import subprocess
import json
import logging
from os import listdir
from os.path import isfile, join

# TODO(AG): Move all configs under index, including relative path - for
# easier testing
editor_app = "suplemon"
data_dir = "./data/"

class Main():


    def process_flags(self, arguments):
        """Send process flow in the right function."""

        # If -n [note_name] is passed, create a note
        if arguments.name:
            self.edit_note(arguments.name)
        elif arguments.list:
            self.list_notes()

    def check_app_dir_initialized(self):
        """Make sure folder is ready to be used."""

    def edit_note(self, name):
        """Edits a note."""
        notevc = NoteVC(name)
        notevc.edit_text()

    def list_notes(self):
        notes_files = self.get_notes_files(data_dir)
        for n in notes_files:
            note = NoteVC(n)
            note.short_print()

    def get_notes_files(self, directory):
        return [f for f in listdir(directory) if isfile(join(directory, f))]


class NoteVC():
    file_path = ""
    note = None

    def __init__(self, name):
        self.file_path = os.path.join(data_dir, name)
        try:
            with open(self.file_path, "r") as note_file:
                text = note_file.read()
        except:
            text = ""
        self.note = Note(name, text)

    def edit_text(self):
        """Launch the editor on the note"""
        edited_text = open_editor(self.note.get_text())
        self.note.set_text(edited_text)
        self.save_note()

    def save_note(self):
        with open(self.file_path, "w") as note_file:
            note_file.write(self.note.get_text())

    def short_print(self):
        """Print a short summary of the note."""
        string = "{}:{}".format(self.note.name[:30],self.note.get_text()[:50])
        print(string)

    def long_print(self):
        """Print the full note data."""
        string = "{}\n=====================\n{}\n".format(self.note.name,self.note.get_text())
        print(string)

class Note():
    name = ""
    text = ""

    def __init__(self, name, text):
        self.name = name
        self.text = text

    def get_text(self):
        return self.text

    def set_text(self, new_text):
        self.text = new_text


def open_editor(string):
    """Edit some text in a temporary file"""
    tmp_path = '/tmp/nap_tmp'
    with open(tmp_path, "w") as tmp:
        tmp.write(string)
    subprocess.call([editor_app, tmp_path])
    with open(tmp_path, 'r') as tmp:
        new_string = tmp.read()
    return new_string

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="nap")

    # TODO (AG) Figure out how to document empty args (will create a perm
    # without name). Once thats done, change parse_known_args for parse_args.
    parser.add_argument("-n", "--name", type=str, metavar="NAME",
                        nargs="?", help="Create or edit a note")
    parser.add_argument("-l", "--list", action='store_true',
                        help="List notes")

    args = parser.parse_args()

    main = Main()
    main.process_flags(args)
