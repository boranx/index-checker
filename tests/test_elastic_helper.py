import unittest
import sys
import datetime
import time
import mock
import os
import pytest

sys.path.append("../")
sys.path.append("../src")

from src.elastic_helper import ElasticHelper

class ElasticHelperTests(unittest.TestCase):
    def test_should_validate_get_index_from_map_returns_valid(self):
        dummy = {'dummy-index-12-02-2019-01-06-46': {'aliases': {'dummy_alias': {}}}}
        result = ElasticHelper.get_index_from_map(dummy)
        self.assertEqual(result, "dummy-index-12-02-2019-01-06-46")

    def test_should_validate_get_index_from_map_returns_sys_exit_when_ex_occurs(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e, self.assertLogs(level='ERROR') as log:
            dummy = {}
            _ = ElasticHelper.get_index_from_map(dummy)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1
        self.assertEqual(log.output, ["ERROR:Elastic Helper:No index found"]) 
        
    def test_should_validate_get_date_from_settings_returns_valid(self):
        dummy = {
            'dummy-12-02-2019-01-06-46': {
                'settings': {
                    'index': {
                        'mapping': {
                            'total_fields': {
                                'limit': '5000'
                            }
                        },
                        'refresh_interval': '10s',
                        'number_of_shards': '5',
                        'provided_name': 'dummy-12-02-2019-01-06-46',
                        'max_result_window': '250000',
                        'creation_date': '1549922806880',
                        'max_slices_per_scroll': '5000',
                        'store': {
                            'preload': ['*']
                        }
                    }
                }
            }
        }
        result = ElasticHelper.get_date_from_settings(
            "dummy-12-02-2019-01-06-46", dummy)
        self.assertEqual(result, "12-02-2019 01:06:46")

    def test_should_validate_get_date_from_settings_prints_log_when_ex_occurs(self):
        dummy = {"wrong":"case"}
        with self.assertLogs(level='ERROR') as log:
            _ = ElasticHelper.get_date_from_settings(
                "dummy-12-02-2019-01-06-46", dummy)
            self.assertEqual(log.output, ["ERROR:Elastic Helper:Failed while getting index date"])

    def test_should_validate_get_date_from_settings_returns_negative_1_when_ex_occurs(self):
        dummy = {"wrong":"case"}
        result = ElasticHelper.get_date_from_settings(
            "dummy-12-02-2019-01-06-46", dummy)
        self.assertEqual(-1, result)

    def test_should_validate_get_doc_count_from_settings_returns_valid(self):
        dummy = {'count': 3559393, '_shards': {'total': 10,
                                               'successful': 10, 'skipped': 0, 'failed': 0}}
        result = ElasticHelper.get_doc_count_from_settings(dummy)
        self.assertEqual(result, 3559393)

    def test_should_validate_get_doc_count_from_settings_prints_log_when_ex_occurs(self):
        dummy = {"wrong":"case"}
        with self.assertLogs(level='ERROR') as log:
            _ = ElasticHelper.get_doc_count_from_settings(dummy)
            self.assertEqual(log.output, ["ERROR:Elastic Helper:Failed while getting document count"]) 

    def test_should_validate_get_doc_count_from_settings_returns_negative_1_when_ex_occurs(self):
        dummy = {"wrong":"case"}
        result = ElasticHelper.get_doc_count_from_settings(dummy)
        self.assertEqual(-1, result)