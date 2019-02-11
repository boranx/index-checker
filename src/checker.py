import logging
import argparse
import sys
import json
import os
import datetime

from src.slack import Slack
from src.elastic import ElasticSearchService, AtomicValidateIndex
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

    def gather(self, ip, parser_index):
        indexList = []
        elasticsearch = ElasticSearchService(ip)
        for one in self.__parsed[parser_index]['aliases']:
            selected_env = self.__parsed[parser_index]['env']
            requested_day = self.__parsed[parser_index]['aliases'][one]['day']
            requested_document = self.__parsed[parser_index]['aliases'][one]['document']
            selected_index = elasticsearch.get_index_of_alias(one)
            index = AtomicValidateIndex(selected_index, ip, selected_env, elasticsearch.get_index_date(
                selected_index), elasticsearch.get_doc_count(selected_index),requested_day, requested_document)
            indexList.append(index)
        return indexList

    def validate(self):
        for i in range(len(self.__parsed)):
            try:
                selected_ip = self.__parsed[i]['elastic']
                listOfIndex = self.gather(selected_ip, i)
                temp = self.mux_checker(listOfIndex)
                if temp == False:
                    self.__status = False
            except Exception as exc:
                logger.error(str(exc))
        if self.__status == True and self.__slack is not None:
            self.__slack.notify(Printer.success_print())

    def mux_checker(self, listIndex):
        flag = True
        for item in listIndex:
            if (not self.checker(item)):
                flag = False
        if flag is False:
            return False
        return True

    def checker(self, index):
        date = DateController(index.requested_day, index.daytime,
                              datetime.datetime.now())
        if not date.control() or not documentctrl(index.docs, index.requested_document):
            writer = Printer("red", index, index.requested_day, index.requested_document)
            print(writer.pretty_print())
            if self.__slack is not None:
                self.__slack.notify(writer.slack_print())
            return False
        else:
            writer = Printer("green", index, index.requested_day, index.requested_document)
            print(writer.pretty_print())
            return True
