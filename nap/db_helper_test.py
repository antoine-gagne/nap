#!/usr/bin/env python

import unittest

from .db_helper import DbHelper


class TestNewDb(unittest.TestCase):

    db = None

    def setUp(self):
        self.db = DbHelper()
        self.db.initialize_db()

    def tearDown(self):
        self.db._close()

    def test_new_db(self):
        # Note has already been initialized in setUp
        # Check list of columns or something
        pass

    def test_db_persistence(self):
        note_name = "notename"
        note_text = "notetext"
        self.db.create_note(note_name, note_text)

        self.db._close()
        self.db = DbHelper()

        text = self.db.get_note_text(note_name)
        self.assertEqual(note_text, text)

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
        self.assertEqual(notes_list[0], note_name1)

    def test_create_note(self):
        note_name = "notename"
        note_text = "notetext"
        self.db.create_note(note_name, note_text)
        db_text = self.db.get_note_text(note_name)
        self.assertEqual(db_text, note_text)

    def test_update_new_note(self):
        note_name = "notename"
        note_text = "notetext"
        self.db.update_note_text(note_name, note_text)
        db_text = self.db.get_note_text(note_name)
        self.assertEqual(db_text, None)

    def test_update_note(self):
        note_name = "notename"
        note_text_initial = "notetext"
        note_text_final = "NoTeTeXt"
        self.db.create_note(note_name, note_text_initial)
        self.db.update_note_text(note_name, note_text_final)
        db_text = self.db.get_note_text(note_name)
        self.assertEqual(db_text, note_text_final)

    def test_add_and_check_keywords(self):
        note_name = "notename"
        note_text = "notetext"
        kws = ['kw1', 'kw2']
        self.db.create_note(note_name, note_text)
        self.db.add_note_keywords(note_name, kws)
        kw = self.db.get_note_keywords(note_name)
        self.assertEqual(kw, kws)

    def test_keywords_filtering(self):
        kw1 = "kw1"
        kw2 = "kw2"
        note_name = "note1"
        note_text = "notetext1"
        kws = [kw1]
        self.db.create_note(note_name, note_text, keywords=kws)
        note_name = "note2"
        note_text = "notetext2"
        kws = [kw1]
        self.db.create_note(note_name, note_text, keywords=kws)
        note_name = "note3"
        note_text = "notetext3"
        kws = [kw2]
        self.db.create_note(note_name, note_text, keywords=kws)
        note_name = "note4"
        note_text = "notetext4"
        self.db.create_note(note_name, note_text)
        notes = self.db.get_notes_list([kw1])
        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[0], 'note1')

    def test_note_exists(self):
        note_name = "notename"
        note_text_initial = "notetext"
        self.db.create_note(note_name, note_text_initial)
        self.assertEqual(True, self.db.note_exists(note_name))
        self.assertEqual(False, self.db.note_exists("unlikely_note_name"))

    def test_note_delete(self):
        note_name = "notename"
        note_text_initial = "notetext"
        self.db.create_note(note_name, note_text_initial)
        self.db.delete_note(note_name)
        self.assertEqual(len(self.db.get_notes_list()), 0)

if __name__ == '__main__':
    unittest.main()
