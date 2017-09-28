import unittest

from index_helper import IndexHelper

test_db_file = "./testdb.db"


class TestNewDb(unittest.TestCase):

    db = None

    def setUp(self):
        self.db = IndexHelper(test_db_file)
        self.db.initialize_db()

    def tearDown(self):
        self.db._close()

    def test_new_db(self):
        # Note has already been initialized in setUp
        # Check list of columns or something
        pass

    def test_create_note(self):
        note_name = "notename"
        note_text = "notetext"
        self.db.create_note(note_name, note_text)
        db_text = self.db.get_note_text(note_name)
        self.assertEqual(db_text, note_text)

if __name__ == '__main__':
    unittest.main()
