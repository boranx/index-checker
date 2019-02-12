import json
import sys
import logging
import datetime

from elasticsearch import Elasticsearch
from src.elastic_helper import ElasticHelper

logging.basicConfig()
logger = logging.getLogger("Elastic")


class ElasticSearchService:
    def __init__(self, elasticsearch_ip_address):
        self.elasticSearch = Elasticsearch(
            elasticsearch_ip_address, maxsize=100)

    def get_index_of_alias(self, alias_name):
        return ElasticHelper.get_index_from_map(self.elasticSearch.indices.get_alias(alias_name))

    def check_exist(self, name):
        if self.elasticSearch.indices.exists(index=name):
            return True
        return False

    def get_index_date(self, index):
        return ElasticHelper.get_date_from_settings(index, self.elasticSearch.indices.get_settings(index))

    def get_doc_count(self, index):
        return ElasticHelper.get_doc_count_from_settings(self.elasticSearch.count(index))


class AtomicValidateIndex:
    def __init__(self, name, ip, env, daytime, docs, requested_day, requested_document):
        self.name = name
        self.ip = ip
        self.env = env
        self.daytime = daytime
        self.docs = docs
        self.requested_day = requested_day
        self.requested_document = requested_document

    def get_object(self):
        return self
