import datetime
from typing import List, Dict

CHRONOS_START = "CHRONOS_START"
CHRONOS_STOP = "CHRONOS_STOP"

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

    def __str__(self):
        output = "===== Chronos Counter =====:\n"
        output += f"Name:               {self.name}\n"
        output += f"Log:                {self.log}\n"
        output += f"Start:              {self.start}\n"
        output += f"Stop Condition:     {self.stop if self.stop != None else 'Not set'}\n"
        output += f"Valid:              {self.stillValid() if self.stop != None else 'Not set'} - {datetime.datetime.now()}\n"
        output += "==============="
        return output

class Chronos:

    logPath: str
    timeMarks: List[ChronosCounter]

    timeLimit: int
    rootTime: datetime.datetime

    def __init__ (self, logPath: str, timeLimit: int):
        self.logPath = logPath
        self.timeMarks = []
        self.timeLimit = timeLimit
        self.rootTime = datetime.datetime.now()

    def printLog(self, message: str):
        print("bla")

    def stillValid(self):
        return (datetime.datetime.now() - self.rootTime).total_seconds() < self.timeLimit

    def startCounter(self, name: str, log: bool = True):
        self.timeMarks.append(ChronosCounter(name = name, log = log))
        if(log):
            self.printLog(f"{CHRONOS_START}: {name}")

    def stopCounter(self):
        if(len(self.timeMarks) > 0):
            last = self.timeMarks.pop()
            if(last.log):
                self.printLog(f"{CHRONOS_STOP}: {last.name}")

    def __str__(self):
        output = "===== Chronos Manager =====\n"
        output += f"Root time:  {self.rootTime}\n"
        output += f"Time limit: {self.timeLimit}\n"
        output += f"Valid:      {self.stillValid()} ({datetime.datetime.now()})\n"
        output += f"Size:       {len(self.timeMarks)}\n"
        output += "List:       "
        for chronosCounter in self.timeMarks:
            output += f" '{chronosCounter.name}'"
        output += "\n==============="
        return output
            