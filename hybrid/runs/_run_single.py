import random

def run_single(self, worse:bool = False, better:bool = False, equal:bool = False): #this is random

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

def testAndGet_single_fixed(self, nurse, day):

    if not (day in self.helperVariables.workingDays[nurse]):
        return False, None

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
            return True, {"n": nurse, "d": day, "s": newShift}

        options.remove(opt)

    return False, None