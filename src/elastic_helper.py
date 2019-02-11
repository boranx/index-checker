import logging
import sys

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