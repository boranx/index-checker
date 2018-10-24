import unittest
import datetime
import sys

from mock import patch, MagicMock

sys.path.append("../")
sys.path.append("../src")

from src.validators.date import DateController
from src.validators.document import documentctrl

class ValidatorsServiceTests(unittest.TestCase):
    
    def setUp(self):
        self.date = datetime.datetime(2018, 10, 8, 21, 41, 43)

    def test_should_validate_date_today(self):
        daytime = "08-10-2018"
        given = 3
        result = DateController(given,daytime,self.date).control()
        self.assertEqual(True, result)
        
    def test_should_validate_old_date(self):
        daytime = "04-10-2018"
        given = 3
        result = DateController(given,daytime,self.date).control()
        self.assertEqual(False, result)

    def test_should_validate_valid_date(self):
        daytime = "06-10-2018"
        given = 3
        result = DateController(given,daytime,self.date).control()
        self.assertEqual(True, result)

    def test_should_validate_given_time_range(self):
        daytime = "15-09-2018"
        given = 30
        result = DateController(given,daytime,self.date).control()
        self.assertEqual(True, result)
    
    def test_should_validate_document_count_in_valid_range(self):
        actual = 1000
        requested = 1500
        result = documentctrl(actual,requested)
        self.assertFalse(result)

    def test_should_validate_document_count_equals(self):
        actual = 1000
        requested = 1000
        result = documentctrl(actual,requested)
        self.assertTrue(result)