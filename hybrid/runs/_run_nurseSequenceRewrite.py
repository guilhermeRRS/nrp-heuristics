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

def run_nurseSequenceRewrite(self, rangeOfSequences:int, numberOfTries:int , worse:bool = False, better:bool = False, equal:bool = False, weight:bool = False): #this is random

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
    
    dayStart, dayEnd = self.getRangeRewrite(nurse, day, rangeOfSequences)
    
    workLoadWithoutSeq, minWorkload, maxWorkload, maximumDaysWorking, minimumDaysWorking, numberBefore = self.min_max_forRewrite(nurse, dayStart, dayEnd)

    smaller = 0
    bigger = 0

    tries = 0
    while tries < numberOfTries:
        print(smaller, bigger)
        s, newStructure, workingDays = self.generate_structure(nurse, dayStart, dayEnd, workLoadWithoutSeq, minWorkload, maxWorkload, maximumDaysWorking, minimumDaysWorking, numberBefore, smaller, bigger)

        if s:
            forbidden = [i for i, x in enumerate(self.nurseModel.data.parameters.m_max[nurse]) if x == 0]
            s, smaller, bigger, newCover = self.generate_cover(newStructure, workingDays, forbidden, nurse, dayStart, dayEnd, workLoadWithoutSeq, minWorkload, maxWorkload, maxTries = 100)
        tries += 1
        
    raise Exception("Stop") 