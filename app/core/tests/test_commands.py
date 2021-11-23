from django.db.utils import OperationalError
from django.core.management import call_command
from django.test import TestCase

from unittest.mock import patch


class CommandTests(TestCase):
    def test_wait_for_db_ready(self):
        """test waiting for db when db is valid"""
        # override the connection state to true
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            # count call, should be only once
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """testing wait for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # try for five times, if 6th time success, return true
            gi.side_effect = [OperationalError]*5+[True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
