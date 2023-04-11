import datetime


def print_ChronosCounter(obj):

    output = f"===== CHRONOS_COUNTER =====:\n"
    output += f"Name:               {obj.name}\n"
    output += f"Log:                {obj.log}\n"
    output += f"Start:              {obj.start}\n"
    output += f"Stop Condition:     {obj.stop if obj.stop != None else 'Not set'}\n"
    output += f"Valid:              {obj.stillValid() if obj.stop != None else 'Not set'} - {datetime.datetime.now()}\n"
    output += f"TimeLeft:           {obj.timeLeft() if obj.stillValid() == True else 0}\n"
    output += "==============="

    return output


def print_Chronos(obj):

    output = f"===== CHRONOS_MANAGER =====\n"
    output += f"Root time:  {obj.rootTime}\n"
    output += f"Time limit: {obj.timeLimit}\n"
    output += f"Valid:      {obj.stillValid()} ({datetime.datetime.now()})\n"
    output += f"Size:       {len(obj.timeMarks)}\n"
    output += "List:       "
    for chronosCounter in obj.timeMarks:
        output += f" '{chronosCounter.name}'"
    output += "\n==============="
    return output