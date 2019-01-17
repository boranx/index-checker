import unittest
import sys

from mock import patch, MagicMock

sys.path.append("../")
sys.path.append("../src")
from src.elastic import ElasticSearchService, AtomicValidateIndex


class ElasticSearchServiceTests(unittest.TestCase):
    def test_should_invoke_get_index_of_alias_method(self):
        alias_name = {'name1': 'value1', 'name2': 'value2', 'name3': 'value3'}
        
        with patch('src.elastic.ElasticSearchService') as mock:
            instance = mock.return_value
            instance.get_index_of_alias.return_value = alias_name

            index = instance.get_index_of_alias("test_alias")

            instance.get_index_of_alias.assert_called_once_with("test_alias")

            self.assertIsNotNone(index)

    def test_should_invoke_check_exist_method(self):        
        with patch('src.elastic.ElasticSearchService') as mock:
            instance = mock.return_value
            instance.check_exist.return_value = True

            status = instance.check_exist("test_index")

            instance.check_exist.assert_called_once_with("test_index")

            self.assertIsNotNone(status)

    def test_should_invoke_get_doc_count_method(self):
        test_index = "test_index"
        doc = "3000"
        
        with patch('src.elastic.ElasticSearchService') as mock:
            instance = mock.return_value
            instance.get_doc_count.return_value = doc

            index = instance.get_doc_count(test_index)

            instance.get_doc_count.assert_called_once_with(test_index)

            self.assertIsNotNone(index)

class AtomicValidateIndexTests(unittest.TestCase):
    def tests_should_validate_index_object_should_valid(self):
        dummy = AtomicValidateIndex("test", "1.1.1.1", "backup", "11-10-2018 02:06:01", "1500","today",1000)
        obj = dummy.get_object()
        self.assertEqual(obj.name, "test")
        self.assertEqual(obj.ip, "1.1.1.1")
        self.assertEqual(obj.requested_day, "today")
        self.assertEqual(obj.requested_document, 1000)