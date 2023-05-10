import random, copy

def run_single(self, worse:bool = False, better:bool = False, equal:bool = False, weight:bool = False): #this is random

    allDays = list(range(0, self.nurseModel.D))
    
    if weight:
        day = random.choices(allDays, weights=self.penalties.worstDays)
        day = day[0]
        possibleNurses = []
        for i in range(self.nurseModel.I):
            if day in self.helperVariables.workingDays[i]:
                possibleNurses.append(i)
                
        if len(possibleNurses) == 0:
            return False, None

        nurse = random.choice(possibleNurses)

    else:
        nurse = random.randint(0, self.nurseModel.I-1)
        day = random.choice(self.helperVariables.workingDays[nurse])

    shiftBefore = "free"
    if day - 1 >= 0:
        shiftBefore = self.shiftFreeMark(self.helperVariables.projectedX[nurse][day-1])
    shifAfter = "free"
    if day + 1 < self.nurseModel.D:
        shifAfter = self.shiftFreeMark(self.helperVariables.projectedX[nurse][day+1])
    
    options = copy.deepcopy(self.helperVariables.oneInnerJourney_rt[shiftBefore][shifAfter])
    
    if len(options) - 1 == 0:
        return False, None

    oldShift = self.helperVariables.projectedX[nurse][day]
    
    options.remove({"s": [oldShift], "w": self.computeLt([oldShift])})
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

def const2_verify(self, nurse, day, shift):

    if not (day in self.helperVariables.workingDays[nurse]):
        return False

    shiftBefore = "free"
    if day - 1 >= 0:
        shiftBefore = self.shiftFreeMark(self.helperVariables.projectedX[nurse][day-1])
    shifAfter = "free"
    if day + 1 < self.nurseModel.D:
        shifAfter = self.shiftFreeMark(self.helperVariables.projectedX[nurse][day+1])
    
    options = self.helperVariables.oneInnerJourney_rt[shiftBefore][shifAfter]

    if len(options) == 0:
        return False
    
    for opt in options:
        if opt["s"] == shift:
            return True
    return False