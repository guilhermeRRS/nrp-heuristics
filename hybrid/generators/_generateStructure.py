import random

def generate_structure(self, nurse, dayStart, dayEnd, workLoadWithoutSeq, minWorkload, maxWorkload, maximumDaysWorking, minimumDaysWorking, numberBefore, smaller, bigger):

    if numberBefore < minimumDaysWorking:
        numberBefore = minimumDaysWorking
    if numberBefore > maximumDaysWorking:
        numberBefore = maximumDaysWorking

    newStructure = []
    workingDays = []

    iter = dayStart
    if dayStart == 0:
        while random.random() >= 0.5:
            newStructure.append(0)
            iter += 1

    while len(workingDays) < dayEnd - dayStart and maximumDaysWorking - len(workingDays) >= self.nurseModel.data.parameters.c_min[nurse]:
        daysToWork = random.randint(self.nurseModel.data.parameters.c_min[nurse], min(self.nurseModel.data.parameters.c_max[nurse], maximumDaysWorking - len(workingDays)))
        nextN_i = -1
        ableToWork = 0
        for d in range(iter, iter + daysToWork):
            if d in self.nurseModel.data.sets.N_i[nurse]:
                nextN_i = d
                break
            else:
                ableToWork += 1
        if nextN_i >= 0:
            if ableToWork >= self.nurseModel.data.parameters.c_min[nurse]:
                daysToWork = ableToWork
            else:
                daysToWork = 0
        for d in range(daysToWork):
            workingDays.append(iter)
            newStructure.append(1)
            iter += 1
        daysToFree = self.nurseModel.data.parameters.o_min[nurse]
        for d in range(daysToFree):
            newStructure.append(0)
            iter += 1
        while random.random() >= 0.5:
            newStructure.append(0)
            iter += 1

    #here we set the right size
    while iter <= dayEnd:
        newStructure.append(0)
        iter += 1

    iter -= 1
    while iter > dayEnd:
        newStructure.pop()
        if iter in workingDays:
            workingDays.remove(iter)
        iter -= 1

    #here we garantee the interval will fit without break any restriction
    iter = len(newStructure) - 1
    daysFree = 0
    if dayEnd < self.nurseModel.D - 1:
        while iter >= 0:
            if newStructure[iter] == 0:
                daysFree += 1
            else:
                break
            iter -= 1
        if daysFree < self.nurseModel.data.parameters.o_min[nurse]:
            iter = len(newStructure) - 1
            daysFree = 0
            while daysFree < self.nurseModel.data.parameters.o_min[nurse]:
                if newStructure[iter] != 0:
                    newStructure[iter] = 0
                    workingDays.remove(iter+dayStart)
                daysFree += 1
                iter -= 1

            #now we verify if the change didnt affect the minimum number of days working
            lastDayWorking = workingDays[-1]
            mustBeworking = lastDayWorking - self.nurseModel.data.parameters.c_min[nurse] + 1
            if not (mustBeworking in workingDays):
                iter = lastDayWorking - dayStart
                while iter >= 0:
                    if newStructure[iter] == 0:
                        break
                    else:
                        newStructure[iter] = 0
                        workingDays.remove(iter+dayStart)

    self.calibrate(newStructure, workingDays, numberBefore, smaller, bigger, dayStart, dayEnd, nurse)

    numberOfDaysWorking = sum(newStructure)
    if numberOfDaysWorking < minimumDaysWorking or numberOfDaysWorking > maximumDaysWorking:
            return False, None, None

    #here we verify restriction 10 -> days thar the nurse must rest
    '''
    for day in self.nurseModel.data.sets.N_i[nurse]:
        if day in workingDays:
            input("++")
            return False, None, None
    input("--")'''
    return True, newStructure, workingDays
    
def calibrate(self, newStructure, workingDays, numberBefore, smaller, bigger, dayStart, dayEnd, nurse):
    print(newStructure, workingDays)
    print(numberBefore, smaller, bigger)
    print(dayStart, dayEnd)
    smaller += 1
    bigger += 1

    if smaller / bigger > 1.8 or bigger / smaller > 1.8:        
        durationOfJourneys = []

        iter = dayStart
        while iter <= dayEnd:
            
            sizeWork = 0
            if newStructure[iter-dayStart] == 1:
                firstJourney = iter
                while iter <= dayEnd and newStructure[iter-dayStart] == 1:
                    sizeWork += 1
                    iter += 1
                lastJourney = iter - 1
                durationOfJourneys.append({"d": sizeWork, "f": firstJourney, "l": lastJourney})
            else:
                iter += 1

    if smaller / bigger > 1.8 or len(workingDays) < numberBefore - 2: # about 65 smaller for 35 bigger, so there is a bigger tendency for a smaller number of days
        if len(workingDays) < numberBefore:
            return self.insertMode(newStructure, workingDays, numberBefore, durationOfJourneys, nurse)
    if bigger / smaller > 1.8 or len(workingDays) > numberBefore + 2:
        if len(workingDays) > numberBefore:
            return self.removeMode(newStructure, workingDays, numberBefore, durationOfJourneys, nurse)



    return newStructure, workingDays

def insertMode(self, newStructure, workingDays, numberBefore, durationOfJourneys, nurse):
    
    if len(durationOfJourneys) >= 2:

        iter = 0
        while iter < 100:
            journey_index = random.randint(0,len(durationOfJourneys)-1)
            journey = durationOfJourneys[journey_index]
            if journey["f"] == 0:
                print(journey)
            elif journey["f"] == self.nurseModel.D:

            else:

            if durationOfJourneys[journey]["d"] < self.nurseModel.data.parameters.c_max[nurse]:
                print(durationOfJourneys[journey])
                input("##")
    
    else:

        #aqui precisa tentar expandir considerando-se somente uma ou nenhuma
    
def removeMode(self, newStructure, workingDays, numberBefore, durationOfJourneys, nurse):
    print("@@")
    input(durationOfJourneys)