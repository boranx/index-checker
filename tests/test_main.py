import unittest
import sys
import os

sys.path.append("../")
sys.path.append("../src")
from src.checker import Checker
from mock import patch, MagicMock
from src.elastic import ElasticSearchService

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

