import json
import sys
import logging
from elasticsearch import Elasticsearch
from elastic_helper import ElasticHelper
import datetime

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
        try:
            settings = self.elasticSearch.indices.get_settings(index)
            parsed = json.loads(json.dumps(settings))
            timestamp = parsed[index]['settings']['index']['creation_date']
            fmt = "%d-%m-%Y %H:%M:%S"
            # local time
            t = datetime.datetime.fromtimestamp(float(timestamp)/1000.)
        except:
            logger.error(str("Failed while getting index date"))
        return t.strftime(fmt)

    def get_doc_count(self, index):
        try:
            settings = self.elasticSearch.count(index)
            parsed = json.loads(json.dumps(settings))
            document_count = parsed['count']
        except:
            logger.error(str("Failed while getting document count"))
        return document_count


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