import logging
import json
import sys
import datetime

logging.basicConfig()
logger = logging.getLogger("Elastic Helper")

class ElasticHelper:
    @staticmethod
    def get_index_from_map(index_map):
        index = ""
        try:
            key, _ = index_map.popitem()
            index = key
        except:
            logger.error(str("No index found"))
            sys.exit(1)
        return index
    
    @staticmethod
    def get_date_from_settings(index, settings):
        try:
            parsed = json.loads(json.dumps(settings))
            timestamp = parsed[index]['settings']['index']['creation_date']
            fmt = "%d-%m-%Y %H:%M:%S"
            # local time
            t = datetime.datetime.fromtimestamp(float(timestamp)/1000.)
            return t.strftime(fmt)
        except:
            logger.error(str("Failed while getting index date"))
            return -1

    @staticmethod
    def get_doc_count_from_settings(settings):
        try:
            parsed = json.loads(json.dumps(settings))
            document_count = parsed['count']
            return document_count
        except:
            logger.error(str("Failed while getting document count"))
            return -1