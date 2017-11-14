import time
import re
import json

from logster.logster_helper import MetricObject, LogsterParser
from logster.logster_helper import LogsterParsingException

class JSONLogster(LogsterParser):

    def __init__(self, option_string=None):
        '''Initialize any data structures or variables needed for keeping track
        of the tasty bits we find in the log we are parsing.'''
        self.codes = {}

    def parse_line(self, line):
        '''This function should digest the contents of one line at a time, updating
        object's state variables. Takes a single argument, the line to be parsed.'''

        try:
            j = json.loads(line)
            if j:
                status = 'http_%s' % j['@fields']['status']
                self.codes[status] = self.codes.get(status, 0) + 1
            else:
                raise LogsterParsingException("failed to parse json for line %s" %s)

        except Exception as e:
            raise LogsterParsingException("contents failed with %s" % e)


    def get_state(self, duration):
        '''Run any necessary calculations on the data collected from the logs
        and return a list of metric objects.'''
        self.duration = float(duration)
        objects = []
        for code in self.codes.keys():
            objects.append(MetricObject(code, (self.codes[code] / self.duration), "Responses per sec"))

        # Return a list of metrics objects
        return objects
