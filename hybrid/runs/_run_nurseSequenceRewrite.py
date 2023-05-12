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

def run_nurseSequenceRewrite(self, rangeOfSequences:int, numberOfTries:int , worse:bool = False, better:bool = False, equal:bool = False): #this is random

    allDays = list(range(0, self.nurseModel.D))
    
    nurse = random.randint(0, self.nurseModel.I-1)
    day = random.choice(self.helperVariables.workingDays[nurse])

    nurse = 0
    day = 0
    
    dayStart, dayEnd = self.getRangeRewrite(nurse, day, rangeOfSequences)
    
    minWorkload, maxWorkload, maximumDaysWorking, minimumDaysWorking = self.min_max_forRewrite(nurse, dayStart, dayEnd)

    range_min = minimumDaysWorking
    range_max = maximumDaysWorking

    tries = 0
    while tries < numberOfTries:
        
        s, newStructure, workingDays = self.generate_structure(nurse, dayStart, dayEnd, maximumDaysWorking, minimumDaysWorking, range_min, range_max)

        if s:
            forbidden = [i for i, x in enumerate(self.nurseModel.data.parameters.m_max[nurse]) if x == 0]
            s, range_min, range_max, newCover = self.generate_cover(newStructure, workingDays, forbidden, nurse, dayStart, dayEnd, minWorkload, maxWorkload, range_min, range_max, maxTries = 100)
        tries += 1
        
    raise Exception("Stop") 