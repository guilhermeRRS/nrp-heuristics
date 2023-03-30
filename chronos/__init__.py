import datetime
import logging
from typing import List, Dict

CHRONOS = "CHRONOS"
INICIALIZATION = "INICIALIZATION"
FINISHED = "FINISHED"

CHRONOS_MARK_START = "CHRONOS_MARK_START"
CHRONOS_MARK_STOP = "CHRONOS_MARK_STOP"

CHRONOS_COUNTER = "CHRONOS_COUNTER"
CHRONOS_MANAGER = "CHRONOS_MANAGER"

class ChronosCounter:

    name: str
    start: datetime.date
    log: bool
    stop: int

    def __init__(self, name: str, log: bool, start: datetime.date = None, stop: int = None):
        self.name = name
        self.log = log
        self.start = datetime.datetime.now() if start == None else start
        self.stop = stop

    def stillValid(self):
        if(self.stop != None):
            return (datetime.datetime.now() - self.start).total_seconds() < self.stop
        return None
    
    def timeLeft(self):
        return self.stop - (datetime.datetime.now() - self.start).total_seconds()

    def __str__(self):
        output = f"===== {CHRONOS_COUNTER} =====:\n"
        output += f"Name:               {self.name}\n"
        output += f"Log:                {self.log}\n"
        output += f"Start:              {self.start}\n"
        output += f"Stop Condition:     {self.stop if self.stop != None else 'Not set'}\n"
        output += f"Valid:              {self.stillValid() if self.stop != None else 'Not set'} - {datetime.datetime.now()}\n"
        output += f"TimeLeft:           {self.timeLeft() if self.stillValid() == True else 0}\n"
        output += "==============="
        return output

class Chronos:

    timeMarks: List[ChronosCounter]

    timeLimit: int
    rootTime: datetime.datetime

    origin: str

    def __init__ (self, timeLimit: int):
        self.timeMarks = []
        self.timeLimit = timeLimit
        self.origin = CHRONOS
        self.rootTime = datetime.datetime.now()

        self.printObj(message = INICIALIZATION, object = self)

    def printObj(self, message: str, object: object):
        logging.info(msg = f"\n>>>>> OBJ | {self.origin} | {datetime.datetime.now()} | {message}\n")
        logging.info(msg = object.__str__())
        logging.info(msg = "\n<<<<<<<<<<<<<<<\n")

    def printMessage(self, message: str, warning: bool = False):
        if warning:
            logging.warning(f"\n>>>>> WARNING | {self.origin} | {datetime.datetime.now()}\n\n{message}\n\n<<<<<<<<<<<<<<<\n")
        else:
            logging.warning(f"\n>>>>> INFO | {self.origin} | {datetime.datetime.now()}\n\n{message}\n\n<<<<<<<<<<<<<<<\n")

    def stillValid(self):
        return (datetime.datetime.now() - self.rootTime).total_seconds() < self.timeLimit
    
    def stillValidRestrict(self):
        return (datetime.datetime.now() - self.rootTime).total_seconds() + 1 < self.timeLimit
    
    def timeLeft(self):
        return self.timeLimit - (datetime.datetime.now() - self.rootTime).total_seconds()

    def startCounter(self, name: str, log: bool = True):
        chronos = ChronosCounter(name = name, log = log, stop = self.timeLeft())
        self.timeMarks.append(chronos)
        if(chronos.log):
            self.printObj(CHRONOS_MARK_START, chronos)

    def stopCounter(self):
        if(len(self.timeMarks) > 0):
            last = self.timeMarks.pop()
            if(last.log):
                self.printObj(CHRONOS_MARK_STOP, last)

    def __str__(self):
        output = f"===== {CHRONOS_MANAGER} =====\n"
        output += f"Root time:  {self.rootTime}\n"
        output += f"Time limit: {self.timeLimit}\n"
        output += f"Valid:      {self.stillValid()} ({datetime.datetime.now()})\n"
        output += f"Size:       {len(self.timeMarks)}\n"
        output += "List:       "
        for chronosCounter in self.timeMarks:
            output += f" '{chronosCounter.name}'"
        output += "\n==============="
        return output
            
    def done(self):
        self.printObj(FINISHED, self)
        return self.__str__()