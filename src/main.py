import logging
import os, sys, optparse
from src.slack import Slack
from src.checker import Checker
from src.parser import Parser
from src.argparser import Arguments

logging.basicConfig()
logger = logging.getLogger("Main")

dirname = os.path.dirname(__file__)
yaml = os.path.join(dirname, '../checker.yaml')
parsed_yaml = Parser(yaml).convert()

def main():
    arguments = Arguments()
    instance = Checker(arguments.return_slack_uri(arguments.get_params()),parsed_yaml)
    instance.validate()
    if instance.get_status() is False:
        logger.error("Exiting with status code 1")
        sys.exit(1)

if __name__ == '__main__':
    main()
