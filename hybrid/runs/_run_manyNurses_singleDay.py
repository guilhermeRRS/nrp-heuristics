import random

def run_manyNurses_singleDay(self, numberOfNurses:int, worse:bool = False, better:bool = False, equal:bool = False): #this is random

    nurse = random.randint(0, self.nurseModel.I - 1)
    day = random.choice(self.helperVariables.workingDays[nurse])

    s, move = self.testAndGet_single_fixed(nurse, day)

    if not s:
        return False, None
    
    moves = [move]
    nurses = [nurse]
    oldShifts = [self.helperVariables.projectedX[nurse][day]]
    newShifts = [move["s"]]

    nurseSpace = list(range(0, self.nurseModel.I))
    nurseSpace.remove(nurse)
    while len(moves) < numberOfNurses and len(nurseSpace) > 0:
        nurse = random.choice(nurseSpace)
        s, move = self.testAndGet_single_fixed(nurse, day)
        if s:
            moves.append(move)
            nurses.append(nurse)
            oldShifts.append(self.helperVariables.projectedX[nurse][day])
            newShifts.append(move["s"])
            break
        nurseSpace.remove(nurse)

    if len(moves) != numberOfNurses:
        return False, None
    
    oldObj = self.penalties.total
    newObj = self.math_manyNurses_singleDay(numberOfNurses, nurses, day, oldShifts, newShifts)
    if self.evaluateFO(oldObj, newObj, worse, better, equal):
        return True, {"n": nurses, "d": day, "o": oldShifts, "n": newShifts}
    return False, None
    

    nurse = random.randint(0, self.nurseModel.I - 1)
    day = random.choice(self.helperVariables.workingDays[nurse])

    shiftBefore = "free"
    if day - 1 >= 0:
        shiftBefore = self.shiftFreeMark(self.helperVariables.projectedX[nurse][day-1])
    shifAfter = "free"
    if day + 1 < self.nurseModel.D:
        shifAfter = self.shiftFreeMark(self.helperVariables.projectedX[nurse][day+1])
    
    options = self.helperVariables.oneInnerJourney_rt[shiftBefore][shifAfter]

    if len(options) == 0:
        return False, None
    
    oldShift = self.helperVariables.projectedX[nurse][day]
    while len(options) > 0:

        opt = random.choice(options)
        newShift = opt["s"][0]
        if self.const_single(nurse, oldShift, newShift):
            oldObj = self.penalties.total
            newObj = self.math_single(nurse, day, oldShift, newShift)
            if self.evaluateFO(oldObj, newObj, worse, better, equal):
                return True, {"n": nurse, "d": day, "s": newShift}

        options.remove(opt)

    return False, None