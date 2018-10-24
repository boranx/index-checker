import logging
import argparse
import sys
import json
import os
import datetime

from src.slack import Slack
from src.elastic import ElasticSearchService, IndexService
from src.parser import Parser
from src.validators.date import DateController
from src.validators.document import documentctrl
from src.printer import Printer

logging.basicConfig()
logger = logging.getLogger("Validator")

dirname = os.path.dirname(__file__)
yaml = os.path.join(dirname, '../checker.yaml')
# slack = Slack("https://hooks.slack.com/services/SLACKHOOKUID")

class Checker:
    def __init__(self):
        self.__status = True

    def get_status(self):
        return self.__status

    def validate(self): 
        parser = Parser(yaml).convert()
        for i in range(len(parser)):
            try:
                selected_ip = parser[i]['elastic']
                elasticsearch = ElasticSearchService(selected_ip)
                for one in parser[i]['aliases']:
                    selected_env = parser[i]['env']
                    requested_day = parser[i]['aliases'][one]['day']
                    requested_document = parser[i]['aliases'][one]['document']
                    selected_index = elasticsearch.get_index_of_alias(one)
                    index = IndexService(selected_index, selected_ip, selected_env, elasticsearch.get_index_date(selected_index), elasticsearch.get_doc_count(selected_index))
                    if (not self.checker(index, requested_day, requested_document)):
                        self.__status = False
            except Exception as exc:
                logger.error(str(exc))

    def checker(self, index, requested_day, requested_docs):
        date = DateController(requested_day, index.daytime, datetime.datetime.now())
        if not date.control() or not documentctrl(index.docs, requested_docs):
            writer = Printer("red", index, requested_day, requested_docs)
            print(writer.pretty_print())
            # slack.notify(writer.slack_print())
            return False
        else:
            writer = Printer("green", index, requested_day, requested_docs)
            print(writer.pretty_print())
            return True
    
