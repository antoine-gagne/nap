#!/usr/bin/env python

"""Semi-integration tests for the cli."""

import unittest

from .cli import App
from .db_helper import DbHelper


class TestNewDb(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.db = DbHelper()
        self.db.initialize_db()

    def tearDown(self):
        pass

    def test_empty_call(self):
        """Not a very good test, but hopefully this passes."""
        self.app.process_flags()

    def test_create_note(self):
        """Create a note, make sure it exists afterwards

        Simulate `nap -n test`
        """
        self.app.process_flags(name="test")
        self.assertEqual(self.db.get_notes_list(), [u'test'])
        self.assertEqual(self.db.get_note_text("test"), "Fake_string")

    def test_list_notes(self):
        """Create some notes and make sure list notes finds them."""
        # Requires an additionnal abstraction layer to be able to hack the view
        # into "displaying" the results to a file.


if __name__ == '__main__':
    unittest.main()
