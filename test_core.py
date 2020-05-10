import unittest
from unittest.mock import MagicMock
from utils.core import *


class TestCore(unittest.TestCase):
    MESSAGES = [
        {
            "TRIGGERS": ["trigger one"],
            "RESPONSES": ["Response One"]
        },
        {
            "TRIGGERS": ["trigger two"],
            "RESPONSES": ["Response Two"]
        }
    ]

    def test_get_random_quote(self):
        self.assertEqual(get_random_quote(self.MESSAGES[0]["RESPONSES"]), "Response One")

    def test_is_keyword_mentioned(self):
        self.assertTrue(is_keyword_mentioned("trigger one", self.MESSAGES[0]["TRIGGERS"]))
        self.assertFalse(is_keyword_mentioned("trigger one", self.MESSAGES[1]["TRIGGERS"]))

        # Ignores capitalization
        self.assertTrue(is_keyword_mentioned("TRIGGER TWO", self.MESSAGES[1]["TRIGGERS"]))
        self.assertFalse(is_keyword_mentioned("TRIGGER TWO", self.MESSAGES[0]["TRIGGERS"]))

    def test_generate_message_response(self):
        self.assertEqual(generate_message_response("trigger one", self.MESSAGES), "Response One")
        self.assertEqual(generate_message_response("trigger two", self.MESSAGES), "Response Two")

    def test_get_username(self):
        from utils.core import get_username
        author_mock = MagicMock()
        author_mock.name = "Peter Parker"

        self.assertEqual(get_username(author_mock), 'Peter Parker')
        self.assertEqual(get_username(None), '[deleted]')


if __name__ == '__main__':
    unittest.main()
