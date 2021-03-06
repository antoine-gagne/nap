#!/usr/bin/env python

"""Note A Problem.

Attributes:
    EDITOR_APP (str): The editor app to use.
"""
import argparse
import logging
import os
import subprocess

from nap import utils

from nap.db.db_helper import DbHelper

main_path = os.path.dirname(os.path.abspath(__file__))

config = utils.get_config_object()

EDITOR_APP = config["app"]["edit_launch_command"]

logger = logging.getLogger('nap_cli')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('nap_log.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

def main():
    """Distribute command line args."""
    parser = argparse.ArgumentParser(prog="nap")

    parser.add_argument("-n", "--name", type=str, metavar="NAME",
                        nargs="?", help="Create or edit a note")
    parser.add_argument("-k", "--keywords", type=str, metavar="KW",
                        nargs="*", help="Use keywords")
    parser.add_argument("-l", "--list", action="store_true",
                        help="List notes")
    parser.add_argument("-d", "--delete", action="store_true",
                        help="Delete a note")

    args = parser.parse_args()
    main = App()
    name = args.name
    logger.debug("Called main with args {}".format(args))
    keywords = args.keywords if args.keywords else []
    list_notes = args.list
    delete = args.delete
    main.process_flags(name, keywords, list_notes, delete)


class App():
    """Handle the inputs and react accordingly."""

    db = None

    def __init__(self):
        App.db = DbHelper()

    def process_flags(self, name="", keywords=[], list_notes=False, delete=False):
        """Send process flow in the right function.

        Args:
          name (str): note's name
          keywords (str[]): note keywords
          list_notes (bool): List notes?
          delete (bool): Delete note? Require name to be passed too.
        """
        if delete:
            self.delete_note(name)
        elif name:
            self.open_note_for_edit(name, keywords)
        else:
            self.print_notes(keywords)

    def delete_note(self, name):
        """Delete a note."""
        NoteFacade.delete_note(name)

    def open_note_for_edit(self, name, keywords):
        """Edit a note.

        Args:
            name (str): The note's name
            keywords (str[]): The note's keywords
        """
        NoteFacade.edit_note(name, keywords)

    def print_notes(self, keywords):
        """Print a list of filtered notes.

        Args:
          keywords (str[]): List of keywords to get notes from.
        """
        NoteFacade.print_notes_filtered_list(keywords)


class NoteFacade():
    """Note Facade.

    List the functionalities available to the App. Aggregates the db_helper
    functions.

    Attributes:
        file_path (str): The path to the note file
        note (Note): Container for the Note data model
    """

    @staticmethod
    def edit_note(name, keywords):
        """Start editing a note's text, saving keywords if note is new."""
        new_note = False
        if not App.db.note_exists(name):
            new_note = True
            App.db.create_note(name, "", keywords)
        else:
            if keywords:
                logger.debug("Keywords are only applied on new notes.")
        text = App.db.get_note_text(name)
        edited_text = open_editor(text)
        if new_note and edited_text == "":
            App.db.delete_note(name)
        App.db.update_note_text(name, edited_text)

    @staticmethod
    def print_notes_filtered_list(keywords):
        """Print notes as filtered by a list of KW."""
        notes_files = App.db.get_notes_list(keywords)
        for n in notes_files:
            NoteFacade.long_print(n)

    @staticmethod
    def short_print(name):
        """Print a short summary of the note on one line."""
        text = App.db.get_note_text(name)
        string = "{}:{}".format(name[:30], text[:50])
        print(string)

    @staticmethod
    def long_print(name):
        """Print the full note data."""
        text = App.db.get_note_text(name)
        kws = App.db.get_note_keywords(name)
        entry_text = '{}'.format(name)
        if kws:
            entry_text += " : "
            entry_text += ", ".join(kws)
        entry_text += "\n=====================\n"
        entry_text += "{}\n".format(text)
        print(entry_text)

    @staticmethod
    def delete_note(name):
        """Delete a note."""
        # TODO(AG): Think of more ways to delete notes (eg. by keywords?)
        App.db.delete_note(name)


def notify(info):
    """Notify user of information."""
    print(info)


def open_editor(text_string):
    """Edit some text in a temporary file.

    Args:
        text_string (str): the initial text string to put in editor

    Returns:
        (str): The string that was written in.
    """
    tmp_path = '/tmp/nap_tmp'
    with open(tmp_path, "w") as tmp:
        if text_string is not None:
            tmp.write(text_string)
        else:
            tmp.write("")
    subprocess.call([EDITOR_APP, tmp_path])
    with open(tmp_path, 'r') as tmp:
        new_string = tmp.read()
    return new_string


def fake_edit():
    """Mock the editor for testing.

    Return:
      str: a predefined string
    """
    return "Fake_string"


if __name__ == "__main__":
    main()
