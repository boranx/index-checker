import unittest
import sys
import datetime
import time
import mock
import os

sys.path.append("../")
sys.path.append("../src")

from mock import patch, MagicMock
from src.parser import Parser
from src.checker import Checker
from src.elastic import ElasticSearchService, AtomicValidateIndex
from contextlib import contextmanager
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

dirname = os.path.dirname(__file__)
yaml = os.path.join(dirname, '../checker.yaml')
parsed_yaml = Parser(yaml).convert()


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
        index = AtomicValidateIndex("test", "1.1.1.1", "prod", today.strftime(
            "%d-%m-%Y %H:%M:%S"), 1500, "today", 1000)
        with captured_output() as (out, err):
            instance = Checker.checker(self, index)
            # This can go inside or outside the `with` block
            output = out.getvalue().strip()
            self.assertIn('OK. Index found :)', output)
            self.assertTrue(instance)

    def test_should_validate_checker_returns_status(self):
        sut = Checker("", "{}")
        sut.__status = True
        self.assertEqual(sut.get_status(), True)

    def test_ensure_that_mux_sends_items_to_checker(self):
        sut = Checker("", "{}")
        today = datetime.date.today()
        test_index = AtomicValidateIndex("test_products", "1.1.1.1", "test", today.strftime(
            "%d-%m-%Y %H:%M:%S"), 1500, "today", 1000)
        test_index2 = AtomicValidateIndex("dummy_products", "1.1.1.1", "test", today.strftime(
            "%d-%m-%Y %H:%M:%S"), 1500, "today", 1000)
        listOfIndexes = []
        listOfIndexes.append(test_index)
        listOfIndexes.append(test_index2)
        flag = sut.mux_checker(listOfIndexes)
        self.assertTrue(flag)

    def test_should_prove_validate_returns_true_if_checks_are_ok(self):
        sut = Checker("", parsed_yaml)
        with mock.patch.object(sut, 'mux_checker', return_value=False) as method:
            with mock.patch.object(sut, 'gather', return_value=[]) as c:
                sut.validate()
                method.assert_called()
                c.assert_called()
                flag = sut.get_status()
                self.assertFalse(flag)

    @mock.patch('src.elastic.ElasticSearchService.get_index_date')
    @mock.patch('src.elastic.ElasticSearchService.get_doc_count')
    @mock.patch('src.elastic.ElasticSearchService.get_index_of_alias')
    def test_should_validate_gather_collects_data_from_es(self, mock_request, mock_docs, mock_date):
        mock_request.return_value = "dummy-products-01-01-2019"
        mock_docs.return_value = 2000
        mock_date.return_value = "18-01-2019 08:04:54"
        sut = Checker("", parsed_yaml)
        IndexList = sut.gather("1.1.1.1", 1)
        self.assertIsNotNone(IndexList)
        self.assertEqual(IndexList[0].ip, "1.1.1.1")
        self.assertEqual(IndexList[0].docs, 2000)
        self.assertEqual(IndexList[0].name, "dummy-products-01-01-2019")
        self.assertEqual(IndexList[0].daytime, "18-01-2019 08:04:54")