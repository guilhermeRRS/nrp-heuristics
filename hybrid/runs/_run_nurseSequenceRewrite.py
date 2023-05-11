import random

def getRangeRewrite(self, nurse, day, rangeOfSequences):
    
    dayStart, dayEnd = self.getSequenceWorkMarks(nurse, day)
    
    iter = dayStart - 1
    while not (iter in self.helperVariables.workingDays[nurse]) and iter >= 0:
        iter -= 1
    dayStart = iter + 1
    
    iter = dayEnd + 1
    while not (iter in self.helperVariables.workingDays[nurse]) and iter < self.nurseModel.D:
        iter += 1
    dayEnd = iter - 1
    
    for i in range(1,rangeOfSequences):
        if i % 2 == 0:
            iter = dayStart - 1
            while iter in self.helperVariables.workingDays[nurse] and iter >= 0:
                iter -= 1
                
            while not (iter in self.helperVariables.workingDays[nurse]) and iter >= 0:
                iter -= 1
            dayStart = iter + 1
        else:
            iter = dayEnd + 1
            while iter in self.helperVariables.workingDays[nurse] and iter < self.nurseModel.D:
                iter += 1
                
            while not (iter in self.helperVariables.workingDays[nurse]) and iter < self.nurseModel.D:
                iter += 1
            dayEnd = iter - 1

    return dayStart, dayEnd

def run_nurseSequenceRewrite(self, rangeOfSequences:int, worse:bool = False, better:bool = False, equal:bool = False, weight:bool = False): #this is random

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

    nurse = 0
    day = 0
    print(self.helperVariables.projectedX[nurse])
    print("_______/",rangeOfSequences)
    dayStart, dayEnd = self.getRangeRewrite(nurse, day, rangeOfSequences)
    
    workLoadWithoutSeq, minWorkload, maxWorkload, maximumDaysWorking, minimumDaysWorking, minimumNumberOfWorkingSequences, maximumNumberOfWorkingSequences = self.min_max_forRewrite(nurse, dayStart, dayEnd)

    print(self.generate_structure(nurse, dayStart, dayEnd, workLoadWithoutSeq, minWorkload, maxWorkload, maximumDaysWorking, minimumDaysWorking, minimumNumberOfWorkingSequences, maximumNumberOfWorkingSequences))
    print(self.generate_structure(nurse, dayStart, dayEnd, workLoadWithoutSeq, minWorkload, maxWorkload, maximumDaysWorking, minimumDaysWorking, minimumNumberOfWorkingSequences, maximumNumberOfWorkingSequences))
    print(self.generate_structure(nurse, dayStart, dayEnd, workLoadWithoutSeq, minWorkload, maxWorkload, maximumDaysWorking, minimumDaysWorking, minimumNumberOfWorkingSequences, maximumNumberOfWorkingSequences))
    print(self.generate_structure(nurse, dayStart, dayEnd, workLoadWithoutSeq, minWorkload, maxWorkload, maximumDaysWorking, minimumDaysWorking, minimumNumberOfWorkingSequences, maximumNumberOfWorkingSequences))
    print(self.generate_structure(nurse, dayStart, dayEnd, workLoadWithoutSeq, minWorkload, maxWorkload, maximumDaysWorking, minimumDaysWorking, minimumNumberOfWorkingSequences, maximumNumberOfWorkingSequences))
    print(self.generate_structure(nurse, dayStart, dayEnd, workLoadWithoutSeq, minWorkload, maxWorkload, maximumDaysWorking, minimumDaysWorking, minimumNumberOfWorkingSequences, maximumNumberOfWorkingSequences))
    print(self.generate_structure(nurse, dayStart, dayEnd, workLoadWithoutSeq, minWorkload, maxWorkload, maximumDaysWorking, minimumDaysWorking, minimumNumberOfWorkingSequences, maximumNumberOfWorkingSequences))
    print(self.generate_structure(nurse, dayStart, dayEnd, workLoadWithoutSeq, minWorkload, maxWorkload, maximumDaysWorking, minimumDaysWorking, minimumNumberOfWorkingSequences, maximumNumberOfWorkingSequences))
    print(self.generate_structure(nurse, dayStart, dayEnd, workLoadWithoutSeq, minWorkload, maxWorkload, maximumDaysWorking, minimumDaysWorking, minimumNumberOfWorkingSequences, maximumNumberOfWorkingSequences))
    print(self.generate_structure(nurse, dayStart, dayEnd, workLoadWithoutSeq, minWorkload, maxWorkload, maximumDaysWorking, minimumDaysWorking, minimumNumberOfWorkingSequences, maximumNumberOfWorkingSequences))
    
    raise Exception("Stop") 
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
    oldShifts["shiftPrePro"] = self.generateShiftPre(oldShifts["s"])

    if len(options) > sizeSampleOptions:
        options = random.sample(options, k = sizeSampleOptions)

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
