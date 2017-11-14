import time
import re

from logster.logster_helper import MetricObject, LogsterParser
from logster.logster_helper import LogsterParsingException

class OOMLogster(LogsterParser):

    def __init__(self, option_string=None):
        '''Initialize any data structures or variables needed for keeping track
        of the tasty bits we find in the log we are parsing.'''
        self.oom = 0
        
    def parse_line(self, line):
        '''This function should digest the contents of one line at a time, updating
        object's state variables. Takes a single argument, the line to be parsed.'''
        print line

        try:
            # Apply regular expression to each line and extract interesting bits.
            if "Out of memory" in line:
                self.oom += 1
            else:
                raise LogsterParsingException("regmatch failed to match")

        except Exception as e:
            raise LogsterParsingException("regmatch or contents failed with %s" % e)


    def get_state(self, duration):
        '''Run any necessary calculations on the data collected from the logs
        and return a list of metric objects.'''
        self.duration = float(duration)
        print "OOM %s" % self.oom

        # Return a list of metrics objects
        return [
            MetricObject("oom", self.oom, "OOM Total"),
        ]
