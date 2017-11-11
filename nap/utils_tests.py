import unittest

from nap import utils

class TestUtils(unittest.TestCase):

    def test_get_config_path(self):
        obj = utils.get_config_object()
        assert obj['app']['db_file']
        assert obj['app']['edit_launch_command']
