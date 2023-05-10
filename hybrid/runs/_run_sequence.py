import random, copy

def getSequenceWorkMarks(self, nurse, day):
    dayStart = day
    dayEnd = day
    iter = dayStart
    while iter in self.helperVariables.workingDays[nurse]:
        iter -= 1
    dayStart = iter + 1
    iter = dayEnd
    while iter in self.helperVariables.workingDays[nurse]:
        iter += 1
    dayEnd = iter - 1
    
    return dayStart, dayEnd

def getOptions(self, shiftBefore, shiftAfter, innerSize):
    if innerSize == 1:
        return self.helperVariables.oneInnerJourney_rt[shiftBefore][shiftAfter]
    elif innerSize == 2:
        return self.helperVariables.twoInnerJourney_rt[shiftBefore][shiftAfter]
    elif innerSize == 3:
        return self.helperVariables.threeInnerJourney_rt[shiftBefore][shiftAfter]
    elif innerSize == 4:
        return self.helperVariables.fourInnerJourney_rt[shiftBefore][shiftAfter]
    elif innerSize == 5:
        return self.helperVariables.fiveInnerJourney_rt[shiftBefore][shiftAfter]
    elif innerSize == 6:
        return self.helperVariables.sixInnerJourney_rt[shiftBefore][shiftAfter]
    raise Exception("Invalid InnerSize")

def run_sequence(self, worse:bool = False, better:bool = False, equal:bool = False, weight:bool = False): #this is random

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

        nurse = random.choices(possibleNurses)
        nurse = nurse[0]

    else:
        nurse = random.randint(0, self.nurseModel.I-1)
        day = random.choice(self.helperVariables.workingDays[nurse])

    dayStart, dayEnd = self.getSequenceWorkMarks(nurse, day)

    shiftBefore = "free"
    if dayStart - 1 >= 0:
        shiftBefore = self.shiftFreeMark(self.helperVariables.projectedX[nurse][dayStart-1])
    shiftAfter = "free"
    if dayEnd + 1 < self.nurseModel.D:
        shiftAfter = self.shiftFreeMark(self.helperVariables.projectedX[nurse][dayEnd+1])
    
    options = copy.deepcopy(self.getOptions(shiftBefore, shiftAfter, dayEnd - dayStart + 1))
    
    if len(options) - 1 == 0:
        return False, None

    oldShifts = self.helperVariables.projectedX[nurse][dayStart:dayEnd+1]
    oldShifts = {"s": oldShifts, "w": self.computeLt(oldShifts)}
    options.remove(oldShifts)
    minWorkload, maxWorkload = self.min_max_possible_workload(nurse, oldShifts["w"])
    while len(options) > 0:

        opt = random.choice(options)
        if opt["w"] >= minWorkload and opt["w"] <= maxWorkload:
            newShifts = opt
            if self.const_sequence(nurse, oldShifts, newShifts):
                oldObj = self.penalties.total
                newObj = self.math_sequence(nurse, dayStart, dayEnd, oldShifts["s"], newShifts["s"])
                if self.evaluateFO(oldObj, newObj, worse, better, equal):
                    return True, {"n": nurse, "d": dayStart, "s": newShifts["s"]}

        options.remove(opt)
        
    return False, None

def run_sequence_fixed(self, nurse, day):

    dayStart, dayEnd = self.getSequenceWorkMarks(nurse, day)

    shiftBefore = "free"
    if dayStart - 1 >= 0:
        shiftBefore = self.shiftFreeMark(self.helperVariables.projectedX[nurse][dayStart-1])
    shiftAfter = "free"
    if dayEnd + 1 < self.nurseModel.D:
        shiftAfter = self.shiftFreeMark(self.helperVariables.projectedX[nurse][dayEnd+1])
    
    options = copy.deepcopy(self.getOptions(shiftBefore, shiftAfter, dayEnd - dayStart + 1))
    
    if len(options) - 1 == 0:
        return False, None

    oldShifts = self.helperVariables.projectedX[nurse][dayStart:dayEnd+1]
    oldShifts = {"s": oldShifts, "w": self.computeLt(oldShifts)}
    options.remove(oldShifts)
    for i in range(len(options)-1,-1,-1):
        opt = options[i]
        newShifts = opt
        if not self.const_sequence(nurse, oldShifts, newShifts):
            options.remove(opt)
    
    if len(options) == 0:
        return False, None

    return True, {"dayStart": dayStart, "length": dayEnd - dayStart + 1, "options": options}