import unittest
import sys
import argparse

from mock import patch, MagicMock

sys.path.append("../")
sys.path.append("../src")
from src.argparser import Arguments


class argParseTestCase(unittest.TestCase):
    def test_should_retrieve_valid_uri_from_cmd(self):
        sys.argv[1:] = ['-s', 'http://dummy_url']
        options = Arguments.get_params()
        self.assertEqual('http://dummy_url', options.SLACK_URL)

    def test_should_retrieve_help_options_from_cmd(self):
        sys.argv[1:] = ['-h']
        with self.assertRaises(SystemExit):
            Arguments.get_params()

    def test_should_validate_empty_flag_for_slack(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-s', dest='SLACK_URL',
                            help='SUT')
        sys.argv[1:] = ['-s', '']
        arguments = Arguments()
        TEST = arguments.return_slack_uri(parser.parse_args())
        self.assertEqual('', TEST)

    def test_should_validate_slack_uri_returns_itself(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-s', dest='SLACK_URL',
                            help='SUT')
        sys.argv[1:] = ['-s', 'http://dummy_url']
        arguments = Arguments()
        TEST = arguments.return_slack_uri(parser.parse_args())
        self.assertEqual('http://dummy_url', TEST)