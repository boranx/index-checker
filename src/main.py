import logging
import os, sys, optparse
from src.slack import Slack
from src.checker import Checker

logging.basicConfig()
logger = logging.getLogger("Main")

def main():
    instance = Checker()
    instance.validate()
    if instance.get_status() is False:
        logger.error("Exiting with status code 1")
        sys.exit(1)

if __name__ == '__main__':
    main()
