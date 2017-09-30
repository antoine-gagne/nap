"""Library to help manage the index file stored as a sqlite db."""

import itertools
import sqlite3


class DbHelper():
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
        self._execute(
            "CREATE TABLE keywords (name text, keyword text, FOREIGN KEY(name) REFERENCES notes(name))")
        # TODO(AG) Add one-to-many for note keywords
        # TODO(AG) Add metadata table for settings and other stuff

    def note_exists(self, name):
        """Check if note exists."""
        cursor = self._execute(
            "SELECT count(*) FROM notes WHERE name=?", (name,))
        if cursor.fetchall()[0][0] == 1:
            return True
        else:
            return False

    def create_note(self, name, text, keywords=[]):
        """Create a note with given text and keywords."""
        self._execute("INSERT INTO notes VALUES (?,?)", (name, text,))
        if keywords:
            self.add_note_keywords(name, keywords)

    def update_note_text(self, name, text):
        """Update the text for a note. Does not create the note if inexistant.

        Args:
          name (str): The name of the note to update
          text (str): Text to assign to note
        Return:
          Int: Number of notes updated (likely 0 or 1)
        """
        if self.note_exists(name):
            self._execute("""UPDATE notes set note_text = ?
                             WHERE name=?""", (text, name,))

    def get_note_text(self, name):
        """Return the text for a specific note or None if inexistant."""
        cursor = self._execute("""SELECT note_text FROM notes
                                  WHERE name=?""", (name,))
        text_array = cursor.fetchone()
        if text_array is not None:
            return text_array[0]
        else:
            return None

    def get_notes_list(self, keywords=[]):
        """Get the list of note names."""
        if keywords:
            notes_list_fetched = []
            for k in keywords:
                query = """SELECT DISTINCT n.name
                           FROM notes n JOIN keywords k
                           ON (n.name = k.name)
                           WHERE k.keyword=?"""
                cursor = self._execute(query, [k])
                data = [x[0] for x in cursor.fetchall()]
                notes_list_fetched.extend(data)
        else:
            cursor = self._execute("SELECT name FROM notes")
            notes_list_fetched = cursor.fetchall()
        if len(notes_list_fetched):
            notes_list = [x[0] for x in notes_list_fetched]
        else:
            notes_list = []
        return notes_list

    def delete_note(self, name):
        self._execute("DELETE FROM notes WHERE name = ?", [name])
        self._execute("DELETE FROM keywords WHERE name = ?", [name])

    def add_note_keywords(self, name, keywords):
        """Add list of keywords to a note."""
        combinations = itertools.product([name], keywords)
        for c in combinations:
            self._execute(
                "INSERT INTO keywords (name, keyword) VALUES (?,?)", (c[0], c[1],))

    def get_note_keywords(self, name):
        """Return the list of keywords for a note."""
        cursor = self._execute(
            "SELECT keyword FROM keywords WHERE name = ?", (name,))
        return [x[0] for x in cursor.fetchall()]

    def _show_all_notes(self):
        cursor = self._execute("SELECT * FROM notes")
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
        self.connection.commit()
        return c
