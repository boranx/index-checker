import logging
import argparse
import sys
import json
import os
import datetime

from src.slack import Slack
from src.elastic import ElasticSearchService, IndexService
from src.validators.date import DateController
from src.validators.document import documentctrl
from src.printer import Printer

logging.basicConfig()
logger = logging.getLogger("Checker")


class Checker:
    def __init__(self, slack_uri, parsed):
        self.__status = True
        if slack_uri:
            self.__slack = Slack(slack_uri)
        else:
            self.__slack = None    
        self.__parsed = parsed

    def get_status(self):
        return self.__status

    def validate(self):
        for i in range(len(self.__parsed)):
            try:
                selected_ip = self.__parsed[i]['elastic']
                elasticsearch = ElasticSearchService(selected_ip)
                for one in self.__parsed[i]['aliases']:
                    selected_env = self.__parsed[i]['env']
                    requested_day = self.__parsed[i]['aliases'][one]['day']
                    requested_document = self.__parsed[i]['aliases'][one]['document']
                    selected_index = elasticsearch.get_index_of_alias(one)
                    index = IndexService(selected_index, selected_ip, selected_env, elasticsearch.get_index_date(
                        selected_index), elasticsearch.get_doc_count(selected_index))
                    if (not self.checker(index, requested_day, requested_document)):
                        self.__status = False
            except Exception as exc:
                logger.error(str(exc))
        if self.__status == True and self.__slack is not None:
            self.__slack.notify(Printer.success_print())

    def checker(self, index, requested_day, requested_docs):
        date = DateController(requested_day, index.daytime,
                              datetime.datetime.now())
        if not date.control() or not documentctrl(index.docs, requested_docs):
            writer = Printer("red", index, requested_day, requested_docs)
            print(writer.pretty_print())
            if self.__slack is not None:
                self.__slack.notify(writer.slack_print())
            return False
        else:
            writer = Printer("green", index, requested_day, requested_docs)
            print(writer.pretty_print())
            return True
