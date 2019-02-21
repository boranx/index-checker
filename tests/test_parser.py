import unittest
import sys
import pytest

from mock import patch, MagicMock

sys.path.append("../")
sys.path.append("../src")
from src.parser import Parser


class ParserTest(unittest.TestCase):
    def setUp(self):
        instance = patch('src.parser.Parser')
        parser = instance.start()
        parser("./").convert.return_value = [{'elastic': '1.1.1.1', 'env': 'backup', 'aliases': {'products': {'day': 'today', 'document': 2800000}}}]
        self.result = parser("./").convert.return_value

    def test_convert_should_be_called(self):
        self.assertIsNotNone(self.result)
    
    def test_convert_should_return_valid_yaml(self):
        self.assertIn('1.1.1.1', str(self.result))
        self.assertIn('backup', str(self.result))
        self.assertIn('today', str(self.result))

class ParserTestExceptions(unittest.TestCase):
    def test_should_validate_convert_returns_sys_exit_when_ex_occurs(self):
        dummy = Parser('dummy')
        with pytest.raises(SystemExit) as pytest_wrapped_e, self.assertLogs(level='ERROR') as log:
            _ = dummy.convert()
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1
        self.assertEqual(log.output, ["ERROR:ELastic:Could not open file"]) 