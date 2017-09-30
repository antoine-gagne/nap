"""Note A Problem.

Attributes:
    SQLITE3_DB (str): The db file where info is stored.
    EDITOR_APP (str): The editor app to use.
"""
import argparse
import subprocess

from db_helper import DbHelper

# TODO(AG): Appart from the db file config, move configs in the db, including
# relative path - for easier testing
SQLITE3_DB = "./datadb.db"
EDITOR_APP = "suplemon"


class Main():
    """Create the notes."""
    db = None

    def __init__(self):
        Main.db = DbHelper(SQLITE3_DB)

    def process_flags(self, arguments):
        """Send process flow in the right function.

        Args:
            arguments (argparse.Namespace): The arguments as received from argparse
        """
        # If -n [note_name] is passed, create a note
        name = arguments.name
        keywords = arguments.keywords
        if arguments.name:
            self.edit_note(name, keywords)
        elif arguments.list:
            self.print_list_notes()

    def edit_note(self, name, keywords):
        """Edit a note.

        Args:
            name (str): The note's name
            keywords (str[]): The note's keywords
        """
        NoteFacade.edit_note(name, keywords)

    def print_list_notes(self):
        """Print the list of notes.

        To be improved.
        """
        notes_files = self.db.get_notes_list()
        for n in notes_files:
            note.long_print()


class NoteFacade():
    """Note Facade.

    List the functionalities available to the Main. Aggregates the db_helper
    functions.

    Attributes:
        file_path (str): The path to the note file
        note (Note): Container for the Note data model
    """

    @staticmethod
    def edit_note(name, keywords):
        """Start editing a note's text, saving keywords if note is new."""
        if not Main.db.note_exists(name):
            Main.db.create_note(name, "", keywords)
        text = Main.db.get_note_text(name)
        NoteFacade.edit_text(name, text)

    @staticmethod
    def load_text(note_name):
        """Load the note's text."""
        # TODO(AG): Make lazy loading text property instead.
        return Main.db.get_note_text(note_name)

    @staticmethod
    def edit_text(name, text):
        """Launch the editor on the note."""
        edited_text = open_editor(text)
        NoteFacade.save_note(name, edited_text)

    @staticmethod
    def save_note(name, text):
        """Save the note to file."""
        Main.db.update_note_text(name, text)

    def short_print(self):
        """Print a short summary of the note on one line."""
        string = "{}:{}".format(self.name[:30], self.text[:50])
        print(string)

    def long_print(self):
        """Print the full note data."""
        string = "{}\n=====================\n{}\n".format(
            self.name, self.text)
        print(string)


def open_editor(text_string):
    """Edit some text in a temporary file.

    Args:
        text_string (str): the initial text string to put in editor

    Returns:
        TYPE: Description
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


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="nap")

    parser.add_argument("-n", "--name", type=str, metavar="NAME",
                        nargs="?", help="Create or edit a note")
    parser.add_argument("-k", "--keywords", type=str, metavar="KW",
                        nargs="*", help="Use keywords")
    parser.add_argument("-l", "--list", action='store_true',
                        help="List notes")

    args = parser.parse_args()

    main = Main()
    main.process_flags(args)
