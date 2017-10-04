#!/usr/bin/env python3

"""Semi-integration tests for the cli."""

import unittest

from .cli import App


class TestNewDb(unittest.TestCase):

    def setUp(self):
        self.app = App()

    def tearDown(self):
        pass

    def test_empty_call(self):
        self.app.process_flags(name=None, keywords=None, list_notes=False, delete=False)

    def test_create_note(self):
        self.app.process_flags(name=None, keywords=None, list_notes=False, delete=False)

if __name__ == '__main__':
    unittest.main()
