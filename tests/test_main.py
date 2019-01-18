import unittest
import sys
import os
import mock

sys.path.append("../")
sys.path.append("../src")
from src.checker import Checker
from mock import patch, MagicMock
from src.elastic import ElasticSearchService
from src.main import main

class MainServiceTests(unittest.TestCase):
    def test_should_validate_checker_instance_is_created(self):
        SLACK_URI = "dummy"
        PARSED = "dummy_parsed_string"
        instance = Checker(SLACK_URI,PARSED)
        self.assertIsNotNone(instance)

    def test_should_validate_checker_validations_called(self):
        with patch('src.checker.Checker.validate') as mock:
            instance = mock.return_value
            instance.validate()
            instance.validate.assert_called()

    @mock.patch('src.argparser.Arguments.return_slack_uri')
    @mock.patch('src.checker.Checker.validate')
    def test_should_validate_main_calls_validates(self, mock_validate, mock_params):
        mock_params.return_value = ""
        mock_validate.return_value = False
        main()
        mock_params.assert_called()
        mock_validate.assert_called()
        self.assertRaises(SystemExit)

    @mock.patch('src.argparser.Arguments.return_slack_uri')
    @mock.patch('src.checker.Checker.validate')
    def test_should_validate_main_calls_validate_false(self, mock_validate, mock_params):
        mock_params.return_value = ""
        mock_validate.return_value = True
        main()
        mock_params.assert_called()
        mock_validate.assert_called()
        self.assertRaises(SystemExit)