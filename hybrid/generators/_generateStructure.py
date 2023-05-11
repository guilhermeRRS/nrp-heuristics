import random

def generate_structure(self, nurse, dayStart, dayEnd, workLoadWithoutSeq, minWorkload, maxWorkload, maximumDaysWorking, minimumDaysWorking, minimumNumberOfWorkingSequences, maximumNumberOfWorkingSequences):

    print(nurse, dayStart, dayEnd)
    print(workLoadWithoutSeq, minWorkload, maxWorkload)
    print(maximumDaysWorking, minimumDaysWorking)

    newStructure = []
    workingDays = []

    iter = dayStart
    if dayStart == 0:
        while random.random() >= 0.5:
            newStructure.append(0)
            iter += 1
            
    while len(workingDays) < dayEnd - dayStart and maximumDaysWorking - len(workingDays) >= self.nurseModel.data.parameters.c_min[nurse]:
        daysToWork = 6#(self.nurseModel.data.parameters.c_min[nurse], min(self.nurseModel.data.parameters.c_max[nurse], maximumDaysWorking - len(workingDays)))
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
        
    print(newStructure)
    print(workingDays)

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

    print("N_i",self.nurseModel.data.sets.N_i[nurse])
    print(newStructure)
    print(workingDays)

    #here we verify restriction 10 -> days thar the nurse must rest
    for day in self.nurseModel.data.sets.N_i[nurse]:
        if day in workingDays:
            input("++")
            return False, None, None
    input("--")
    return True, newStructure, workingDays
    