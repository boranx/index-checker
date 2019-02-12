import unittest
import sys
import datetime
import time
import mock
import os

sys.path.append("../")
sys.path.append("../src")

from src.elastic_helper import ElasticHelper


class ElasticHelperTests(unittest.TestCase):
    def test_should_validate_get_index_from_map_returns_valid(self):
        dummy = {'dummy-index-12-02-2019-01-06-46': {'aliases': {'dummy_alias': {}}}}
        result = ElasticHelper.get_index_from_map(dummy)
        self.assertEqual(result, "dummy-index-12-02-2019-01-06-46")

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

    def test_should_validate_get_doc_count_from_settings_returns_valid(self):
        dummy = {'count': 3559393, '_shards': {'total': 10,
                                               'successful': 10, 'skipped': 0, 'failed': 0}}
        result = ElasticHelper.get_doc_count_from_settings(dummy)
        self.assertEqual(result, 3559393)
