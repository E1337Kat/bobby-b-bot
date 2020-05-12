import unittest
from mock import MagicMock
from utils.scheduler import init_message_scheduler


class TestScheduler(unittest.TestCase):

    def test_init_message_scheduler(self):

        client_mock = MagicMock()
        self.assertEqual(init_message_scheduler(None, client_mock), None)


if __name__ == '__main__':
    unittest.main()
