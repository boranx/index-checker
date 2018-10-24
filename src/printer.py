from termcolor import colored

class Printer():
    def __init__(self, color, index, requested_day, requested_docs):
        self._color          = color
        self._index          = index.name
        self._ip             = index.ip
        self._env            = index.env
        self._date           = index.daytime
        self._requested_day  = requested_day
        self._docs           = index.docs
        self._requested_docs = requested_docs
    
    def find_header(self):
        if self._color == 'red':
            return "Status: Fail!!! Index is old !!! :( \n" 
        return "Status: OK. Index found :) \n"
    
    def pretty_print(self):
        header = self.find_header()
        text = f"------------------ \n\n {header} \
            Index Name: %s \n \
            Elastic : %s \n \
            Env: %s \n \
            Creation: %s \n \
            Date must be(within) : %s \n \
            CurrentDocumentCount : %s \n \
            Documents must be higher than: %s \n" % (self._index, self._ip, self._env, self._date, self._requested_day, self._docs, self._requested_docs)
        return colored(text, self._color)

    def slack_print(self):
        header = self.find_header()
        text = f"------------------ \n\n {header} \
            Index Name: %s \n \
            Elastic : %s \n \
            Env: %s \n \
            Creation: %s \n \
            Date must be(within) : %s \n \
            CurrentDocumentCount : %s \n \
            Documents must be higher than: %s \n" % (self._index, self._ip, self._env, self._date, self._requested_day, self._docs, self._requested_docs)
        return text