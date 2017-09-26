"""Takes notes.

Attributes:
    data_dir (str): The location where to store notes.
    editor_app (str): The editor app to use.
"""
import argparse
import json
import logging
import os
import subprocess

# TODO(AG): Move all configs under index, including relative path - for
# easier testing
data_dir = "./data/"
editor_app = "suplemon"


class Main():
    """Create the notes."""

    def process_flags(self, arguments):
        """Send process flow in the right function.

        Args:
            arguments (argparse.Namespace): The arguments as received from argparse
        """
        # If -n [note_name] is passed, create a note
        if arguments.name:
            self.edit_note(arguments.name)
        elif arguments.list:
            self.print_list_notes()

    def check_app_dir_initialized(self):
        """Make sure folder is ready to be used."""

    def edit_note(self, name):
        """Edit a note.

        Args:
            name (str): The note's name
        """
        notevc = NoteVC(name)
        notevc.edit_text()

    def print_list_notes(self):
        """Print the list of notes.

        To be improved.
        """
        notes_files = self.get_notes_files(data_dir)
        for n in notes_files:
            note = NoteVC(n)
            note.short_print()

    def get_notes_files(self, directory):
        """List the note files.

        Args:
            directory (string): The directory where to list files from

        Returns:
            string[]: The list of files found
        """
        return [f for f in os.listdir(directory) if
                os.path.isfile(os.path.join(directory, f))]


class NoteVC():
    """Note view and controller.

    Attributes:
        file_path (str): The path to the note file
        note (Note): Container for the Note data model
    """

    file_path = ""
    note = None

    def __init__(self, name):
        """Create the Note View-Controller.

        Args:
            name (string): the name of the note
        """
        self.file_path = os.path.join(data_dir, name)
        try:
            with open(self.file_path, "r") as note_file:
                text = note_file.read()
        except:
            text = ""
        self.note = Note(name, text)

    def edit_text(self):
        """Launch the editor on the note."""
        edited_text = open_editor(self.note.get_text())
        self.note.set_text(edited_text)
        self.save_note()

    def save_note(self):
        """Save the note to file."""
        with open(self.file_path, "w") as note_file:
            note_file.write(self.note.get_text())

    def short_print(self):
        """Print a short summary of the note on one line."""
        string = "{}:{}".format(self.note.name[:30], self.note.get_text()[:50])
        print(string)

    def long_print(self):
        """Print the full note data."""
        string = "{}\n=====================\n{}\n".format(
            self.note.name, self.note.get_text())
        print(string)


class Note():
    """Note model information.

    Attributes:
        name (str): The Note's name
        text (str): The Note's text
    """

    name = ""
    text = ""

    def __init__(self, name, text):
        """Initialize the note.

        Args:
        name (str): The Note's name
        text (str): The Note's text  # TODO: Make lazy loading
        """
        self.name = name
        self.text = text

    def get_text(self):
        """Get the Note's text.

        Returns:
            string: text
        """
        return self.text

    def set_text(self, new_text):
        """Set the Note's text..

        Args:
            new_text (string): The new Note's text.
        """
        self.text = new_text


def open_editor(text_string):
    """Edit some text in a temporary file.

    Args:
        text_string (str): the initial text string to put in editor

    Returns:
        TYPE: Description
    """
    tmp_path = '/tmp/nap_tmp'
    with open(tmp_path, "w") as tmp:
        tmp.write(text_string)
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
