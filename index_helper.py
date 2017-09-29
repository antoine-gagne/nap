"""Library to help manage the index file stored as a sqlite db."""

import itertools
import sqlite3


class IndexHelper():
    """Manage the connection to the data db."""

    connection = None

    def __init__(self, db_path):
        """Initialize the Index object."""
        self._connect_db(db_path)

    # Public functions

    def initialize_db(self):
        """Initialize the db's tables."""
        self._execute("DROP TABLE IF EXISTS notes")
        self._execute("DROP TABLE IF EXISTS keywords")
        self._execute("CREATE TABLE notes (name text, note_text text)")
        self._execute("CREATE TABLE keywords (name text, keyword text, FOREIGN KEY(name) REFERENCES notes(name))")
        # TODO(AG) Add one-to-many for note keywords
        # TODO(AG) Add metadata table for settings and other stuff

    def create_note(self, name, text):
        """Create a note with given text."""
        self._execute("INSERT INTO notes VALUES (?,?)", (name, text,))

    def update_note_text(self, name, text):
        """Update the text for a note.

        Args:
          name (str): The name of the note to update
          text (str): Text to assign to note
        Return:
          Int: Number of notes updated (likely 0 or 1)
        """
        cursor = self._execute("""UPDATE notes set note_text = ?
                                  WHERE name=?""", (text, name,))
        cursor = self._execute("SELECT changes()")
        return cursor.fetchone()[0]

    def get_note_text(self, name):
        """Return the text for a specific note."""
        cursor = self._execute("""SELECT note_text FROM notes
                                  WHERE name=?""", (name,))
        return cursor.fetchone()[0]

    def get_notes_list(self):
        """Get the list of note names."""
        cursor = self._execute("SELECT name FROM notes")
        return cursor.fetchall()

    def add_note_keywords(self, name, keywords):
        """Add list of keywords to a note."""
        combinations = itertools.product([name], keywords)
        for c in combinations:
            self._execute("INSERT INTO keywords (name, keyword) VALUES (?,?)", (c[0],c[1],))

    def get_note_keywords(self, name):
        """Return the list of keywords for a note."""
        cursor = self._execute("SELECT keyword FROM keywords WHERE name = ?", (name,))
        return [x[0] for x in cursor.fetchall()]

    # Private functions
    def _connect_db(self, db_path):
        """Connect to the database."""
        self.connection = sqlite3.connect(db_path)

    def _close(self):
        self.connection.close()

    def _get_cursor(self):
        """Provide a cursor for the db."""
        return self.connection.cursor()

    def _execute(self, command, arguments=None):
        """Execute a SQL statement on the DB."""
        c = self._get_cursor()
        if arguments:
            c.execute(command, arguments)
        else:
            c.execute(command)
        return c
