import datetime
import logging
from typing import List, Dict
from ._printers import *

CHRONOS_START_MESSAGE = ">>>>>"
CHRONOS_END_MESSAGE = "<<<<<<<<<<<<<<<"

CHRONOS = "CHRONOS"
INICIALIZATION = "INICIALIZATION"
FINISHED = "FINISHED"

CHRONOS_MARK_START = "CHRONOS_MARK_START"
CHRONOS_MARK_STOP = "CHRONOS_MARK_STOP"

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
       
        return print_ChronosCounter(self)

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
        logging.info(msg = f"\n{CHRONOS_START_MESSAGE} OBJ | {self.origin} | {datetime.datetime.now()} | {message}\n")
        logging.info(msg = object.__str__())
        logging.info(msg = F"\n{CHRONOS_END_MESSAGE}n")

    def printMessage(self, message: str, warning: bool = False):
        if warning:
            logging.warning(f"\n{CHRONOS_START_MESSAGE} WARNING | {self.origin} | {datetime.datetime.now()}\n\n{message}\n\n{CHRONOS_END_MESSAGE}\n")
        else:
            logging.warning(f"\n{CHRONOS_START_MESSAGE} INFO | {self.origin} | {datetime.datetime.now()}\n\n{message}\n\n{CHRONOS_END_MESSAGE}\n")

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
        return print_Chronos(self)
            
    def done(self):
        self.printObj(FINISHED, self)
        return self.__str__()