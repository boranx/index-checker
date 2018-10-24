import unittest
import sys
import datetime, time

sys.path.append("../")
sys.path.append("../src")

from mock import patch, MagicMock
from src.checker import Checker
from src.elastic import ElasticSearchService, IndexService
from contextlib import contextmanager
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class CheckerServiceTests(unittest.TestCase):
    def test_should_validate_checker_status(self):
        today = datetime.date.today()
        index = IndexService("test", "1.1.1.1", "prod", today.strftime("%d-%m-%Y %H:%M:%S"), 1500)
        requested_day = "today"
        requested_docs = 1000
        with captured_output() as (out, err):
            instance = Checker.checker(self, index, requested_day, requested_docs)
            # This can go inside or outside the `with` block
            output = out.getvalue().strip()
            self.assertIn('OK. Index found :)', output)
            self.assertTrue(instance)
