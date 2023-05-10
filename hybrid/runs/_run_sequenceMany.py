import random

#if the choosen nurses fails on having at least on alternative sequence each, this function exits
def run_sequenceMany(self, numberOfNurses:int, maxInsideCombinationOf:int = 10000,  worse:bool = False, better:bool = False, equal:bool = False, weight:bool = False):

    allDays = list(range(0, self.nurseModel.D))
    
    if weight:
        day = random.choices(allDays, weights=self.penalties.worstDays)
        day = day[0]
    else:
        day = random.randint(0, self.nurseModel.D-1)

    possibleNurses = []
    for i in range(self.nurseModel.I):
        if day in self.helperVariables.workingDays[i]:
            possibleNurses.append(i)
            
    if len(possibleNurses) < numberOfNurses:
        return False, None
    
    nurses = random.sample(possibleNurses, k = numberOfNurses)
    nursesOptions = []
    earliestDay = self.nurseModel.D
    latestDay = 0
    for nurse in nurses:
        s, nurseOptions = self.run_sequence_fixed(nurse, day)
        if s:
            if earliestDay > nurseOptions["dayStart"]:
                earliestDay = nurseOptions["dayStart"]
            if latestDay < nurseOptions["dayStart"] + nurseOptions["length"] - 1:
                latestDay = nurseOptions["dayStart"] + nurseOptions["length"] - 1
            nursesOptions.append(nurseOptions)
        else:
            break

    if len(nursesOptions) != numberOfNurses:
        return False, None

    '''
    (preenchimento de pré-processamento) -> para olds (the um append no old, conforme insere-se os intervalos)
    Agora, dentro do rol de combinações possíveis, escolhe-se, avalia-se a função objetivo até max
    '''

    oldShifts = [] #notice: this oldShift is differente: it is the inverse of the other oldshifts - first info here is day, latter the nurse (this is useful fo quicker math)
    for d in range(earliestDay, latestDay+1):
        oldShifts.append([])
        for i in range(len(nurses)):
            if d >= nursesOptions[i]["dayStart"] and d < nursesOptions[i]["dayStart"] + nursesOptions[i]["length"]:
                oldShifts[-1].append(self.helperVariables.projectedX[nurses[i]][d])
            else:
                oldShifts[-1].append(-1)

    i = 0
    while i < maxInsideCombinationOf:
        choosenOptions = []
        for j in range(numberOfNurses):
            nurseOption = nursesOptions[j]
            choosenOptions.append({"n": nurses[j], "length": nurseOption["length"], "dayStart": nurseOption["dayStart"], "s": (random.choice(nurseOption["options"]))["s"]})

        newObj = self.math_manyNurses_daySequence(oldShifts, earliestDay, choosenOptions)
        if self.evaluateFO(self.penalties.total, newObj, worse, better, equal):
            return True, {"s": choosenOptions}
        
        i += 1
    return False, None