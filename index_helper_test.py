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

    def test_get_note_text(self):
        note_name = "notename"
        note_text = "notetext"
        self.db.create_note(note_name, note_text)

        text = self.db.get_note_text(note_name)
        self.assertEqual(note_text, text)

    def test_get_note_list(self):
        note_name1 = "notename1"
        note_name2 = "notename2"
        note_name3 = "notename3"
        note_text = "notetext"
        self.db.create_note(note_name1, note_text)
        self.db.create_note(note_name2, note_text)
        self.db.create_note(note_name3, note_text)

        notes_list = self.db.get_notes_list()
        self.assertEqual(len(notes_list), 3)

    def test_create_note(self):
        note_name = "notename"
        note_text = "notetext"
        self.db.create_note(note_name, note_text)
        db_text = self.db.get_note_text(note_name)
        self.assertEqual(db_text, note_text)

    def test_update_new_note(self):
        note_name = "notename"
        note_text = "notetext"
        nb_changes = self.db.update_note_text(note_name, note_text)
        self.assertEqual(nb_changes, 0)

    def test_update_note(self):
        note_name = "notename"
        note_text_initial = "notetext"
        note_text_final = "NoTeTeXt"
        self.db.create_note(note_name, note_text_initial)
        nb_changes = self.db.update_note_text(note_name, note_text_final)
        db_text = self.db.get_note_text(note_name)
        self.assertEqual(db_text, note_text_final)
        self.assertEqual(nb_changes, 1)

    def test_add_and_check_keywords(self):
        note_name = "notename"
        note_text = "notetext"
        kws = ['kw1', 'kw2']
        self.db.create_note(note_name, note_text)
        self.db.add_note_keywords(note_name, kws)
        kw = self.db.get_note_keywords(note_name)

if __name__ == '__main__':
    unittest.main()
