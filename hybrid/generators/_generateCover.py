import itertools


def generate_cover(self, newStructure, workingDays, forbidden, nurse, dayStart, dayEnd, workLoadWithoutSeq, minWorkload, maxWorkload, maxTries:int):

    durationOfJourneys = []

    iter = dayStart
    while iter <= dayEnd:
        
        sizeWork = 0
        if newStructure[iter-dayStart] == 1:
            while newStructure[iter-dayStart] == 1:
                sizeWork += 1
                iter += 1
            durationOfJourneys.append(sizeWork)
        else:
            iter += 1

    tryCounter = 0
    smaller = 0
    bigger = 0
    while tryCounter < maxTries:
        
        theCover = []
        addWorkLoad = 0
        for duration in durationOfJourneys:
            theCover.append(self.getOptionBySize(duration, forbidden))
            addWorkLoad += theCover[-1]["w"]
            theCover[-1] = theCover[-1]["s"]
        if addWorkLoad >= minWorkload and addWorkLoad <= maxWorkload:
            if self.verify_generateCover_mmax(nurse, dayStart, theCover):
                input("!!!")
                return True, smaller, bigger, {"n": nurse, "dayStart": dayStart, "s": theCover, "w": addWorkLoad}
            else:
                input("@@")
        else:
            if addWorkLoad < minWorkload:
                smaller += 1
            if addWorkLoad > maxWorkload:
                bigger += 1
        tryCounter += 1
        
    return False, smaller, bigger, None

def verify_generateCover_mmax(self, nurse, dayStart, theCover):
    print(theCover)
    allShifts = list(itertools.chain.from_iterable(theCover))
    oldShifts = self.helperVariables.projectedX[nurse][dayStart:(dayStart+len(theCover))]
    affectedShifts = list(dict.fromkeys(allShifts))
    for shift in affectedShifts:
        if self.helperVariables.shiftTypeCounter[nurse][shift] - oldShifts.count(shift) + allShifts.count(shift) > self.nurseModel.data.parameters.m_max[nurse][shift]:
            print(self.helperVariables.shiftTypeCounter[nurse][shift], self.nurseModel.data.parameters.m_max[nurse][shift])
            print( oldShifts.count(shift), allShifts.count(shift))
            return False
    return True