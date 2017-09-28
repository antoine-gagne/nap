"""Library to help manage the index file stored as a sqlite db."""

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
        self._execute("CREATE TABLE notes (name text, note_text text)")
        # TODO(AG) Add one-to-many for note keywords
        # TODO(AG) Add metadata table for settings and other stuff

    def create_note(self, name, text):
        """Create a note with given text."""
        self._execute("INSERT INTO notes VALUES (?,?)", (name, text,))

    def get_note_text(self, note_name):
        """Return the text for a specific note."""
        cursor = self._execute("""SELECT note_text FROM notes
                                  WHERE name=?""", (note_name,))
        return cursor.fetchone()[0]

    def get_notes_list(self):
        """Get the list of note names."""
        cursor = self._exectute("SELECT name FROM notes")
        return cursor.fetchall()

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
