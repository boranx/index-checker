import unittest
import sys

sys.path.append("../")
sys.path.append("../src")

from src.printer import Printer
from src.elastic import AtomicValidateIndex

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO



class PrinterServiceTests(unittest.TestCase):
    def test_should_validate_slack_print_returns_valid_text(self):
        index = AtomicValidateIndex("test", "1.1.1.1", "backup", "11-10-2018 02:06:01", "1500","today",1000)
        instance = Printer('red', index, '2', '3000000')
        self.assertIn("11-10-2018 02:06:01", instance.slack_print())
        self.assertIn("3000000", instance.slack_print())
        self.assertIn("2", instance.slack_print())
        self.assertNotIn("red", instance.slack_print())

    def test_should_validate_success_print_returns_valid_text(self):
        result = Printer.success_print()
        self.assertIn("Index Checker succeeded", result)
        self.assertIn("All tests passed", result)