import yaml
import logging
import sys

logging.basicConfig()
logger = logging.getLogger("ELastic")

class Parser:
    def __init__(self, yaml_file):
        self.yaml_file = yaml_file
    
    def convert(self):
        try:
            self.stream = open(self.yaml_file, 'r')
        except:
            logger.error(str("Could not open file"))
            sys.exit(1)
        return yaml.load(self.stream)
