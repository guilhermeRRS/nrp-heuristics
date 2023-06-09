import itertools

def computeLt(self, sequence):
    return sum([self.nurseModel.data.parameters.l_t[sequence[i]] for i in range(len(sequence))])

def generateFromSolution(self):
    print("Generating")
    self.helperVariables.shiftTypeCounter = []
    self.helperVariables.workloadCounter = []
    self.helperVariables.weekendCounter = []
    self.helperVariables.projectedX = []
    self.helperVariables.workingDays = []

    self.penalties.preference_total = 0
    
    self.penalties.numberNurses = []
    self.penalties.worstDays = []
    self.penalties.worstDaysShifts = []
    for d in range(self.nurseModel.D):
        self.penalties.numberNurses.append([])
        self.penalties.worstDays.append(0)
        self.penalties.worstDaysShifts.append([])
        for t in range(self.nurseModel.T):
            self.penalties.numberNurses[-1].append(0)
            self.penalties.worstDaysShifts[-1].append(0)
    
    print("Calculating")
    for i in range(self.nurseModel.I):
        self.helperVariables.shiftTypeCounter.append([])
        self.helperVariables.workloadCounter.append(0)
        self.helperVariables.weekendCounter.append([])
        self.helperVariables.projectedX.append([])
        self.helperVariables.workingDays.append([])
        
        for t in range(self.nurseModel.T):
            self.helperVariables.shiftTypeCounter[-1].append(0)
        
        for d in range(self.nurseModel.D):
            self.helperVariables.projectedX[-1].append(-1)
            for t in range(self.nurseModel.T):
                self.penalties.preference_total += self.nurseModel.data.parameters.p[i][d][t]*self.nurseModel.solution.solution[i][d][t]+self.nurseModel.data.parameters.q[i][d][t]*(1 - self.nurseModel.solution.solution[i][d][t])
            
                self.nurseModel.model.x[i][d][t].ub = self.nurseModel.solution.solution[i][d][t]
                self.nurseModel.model.x[i][d][t].lb = self.nurseModel.solution.solution[i][d][t]

                if self.nurseModel.solution.solution[i][d][t] >= 0.5:
                    self.helperVariables.shiftTypeCounter[-1][t] += 1
                    self.helperVariables.workloadCounter[-1] += self.nurseModel.data.parameters.l_t[t]
                    self.helperVariables.projectedX[-1][d] = t
                    self.helperVariables.workingDays[-1].append(d)
                    self.penalties.numberNurses[d][t] += 1

        for w in range(self.nurseModel.W):
            self.helperVariables.weekendCounter[-1].append(1 if (self.helperVariables.projectedX[-1][7*w+5] + self.helperVariables.projectedX[-1][7*w+6]) > 0.5 else 0)
    
    print("Demanding & setting")
    self.penalties.demand = 0

    r_t_plain = []
    self.helperVariables.oneInnerJourney_rt = {"free": {"free": []}}
    self.helperVariables.twoInnerJourney_rt = {"free": {"free": []}}
    self.helperVariables.threeInnerJourney_rt = {"free": {"free": []}}
    self.helperVariables.fourInnerJourney_rt = {"free": {"free": []}}
    self.helperVariables.fiveInnerJourney_rt = {"free": {"free": []}}
    self.helperVariables.sixInnerJourney_rt = {"free": {"free": []}}

    equivalence = []
    for t in range(self.nurseModel.T):
        equivalence.append(self.nurseModel.data.sets.R_t.index(self.nurseModel.data.sets.R_t[t]))
        for d in range(self.nurseModel.D):
            numberNurses = self.penalties.numberNurses[d][t]
            neededNurses = self.nurseModel.data.parameters.u[d][t]
            addingPenalty = 0
            if numberNurses < neededNurses:
                addingPenalty = (neededNurses - numberNurses)*self.nurseModel.data.parameters.w_min[d][t]
                self.penalties.demand += addingPenalty
            elif numberNurses > neededNurses:
                addingPenalty = (numberNurses - neededNurses)*self.nurseModel.data.parameters.w_max[d][t]
                self.penalties.demand += addingPenalty
            self.penalties.worstDaysShifts[d][t] += addingPenalty
            self.penalties.worstDays[d] += addingPenalty

        r_t_plain.append([i for i, x in enumerate(self.nurseModel.data.sets.R_t[t]) if x == 0])

        self.helperVariables.oneInnerJourney_rt["free"]["free"].append({"s": [t], "w": self.computeLt([t])})

        self.helperVariables.oneInnerJourney_rt["free"][t] = []
        self.helperVariables.oneInnerJourney_rt[t] = {"free": []}
        self.helperVariables.twoInnerJourney_rt["free"][t] = []
        self.helperVariables.twoInnerJourney_rt[t] = {"free": []}
        self.helperVariables.threeInnerJourney_rt["free"][t] = []
        self.helperVariables.threeInnerJourney_rt[t] = {"free": []}
        self.helperVariables.fourInnerJourney_rt["free"][t] = []
        self.helperVariables.fourInnerJourney_rt[t] = {"free": []}
        self.helperVariables.fiveInnerJourney_rt["free"][t] = []
        self.helperVariables.fiveInnerJourney_rt[t] = {"free": []}
        #not needed more, the max of all instances is 6 workDays

        for t2 in range(self.nurseModel.T):
            self.helperVariables.oneInnerJourney_rt[t][t2] = []
            self.helperVariables.twoInnerJourney_rt[t][t2] = []
            self.helperVariables.threeInnerJourney_rt[t][t2] = []
            self.helperVariables.fourInnerJourney_rt[t][t2] = []
            #not needed, the max of all instances is 6 workDays and this is used for 7
            self.helperVariables.fiveInnerJourney_rt[t][t2] = []
    

    self.penalties.total = self.penalties.demand + self.penalties.preference_total

    print("The monster")
    highest_cmax = max(self.nurseModel.data.parameters.c_max)
    self.highest_cmax = highest_cmax

    sizedTwoStarting = {}
    sizedThreeStarting = {}
    sizedFourStarting = {}
    sizedFiveStarting = {}
    sizedSixStarting = {}
    for t in range(self.nurseModel.T):
        sizedTwoStarting[t] = []
        sizedThreeStarting[t] = []
        sizedFourStarting[t] = []
        sizedFiveStarting[t] = []
        sizedSixStarting[t] = []
    
    print("The monster for sized 2")
    sizedTwo = []
    for tStart in range(self.nurseModel.T):
        for tEnd in r_t_plain[tStart]:
            newSequence = [tStart, tEnd]
            sizedTwo.append(newSequence)
            sizedTwoStarting[tStart].append(newSequence)
            
            ##Setting the global vars
            freeFirst = [tStart]
            freeAfter = [tEnd]
            self.helperVariables.oneInnerJourney_rt["free"][tEnd].append({"s": freeFirst, "w": self.computeLt(freeFirst)})
            self.helperVariables.oneInnerJourney_rt[tStart]["free"].append({"s": freeAfter, "w": self.computeLt(freeAfter)})

            self.helperVariables.twoInnerJourney_rt["free"]["free"].append({"s": newSequence, "w": self.computeLt(newSequence)})
    
    print("The monster for sized 3")
    sizedThree = []
    for sequence1 in sizedTwo:
        tEndingFirst = sequence1[-1]
        for sequence2 in sizedTwoStarting[tEndingFirst]:
            newSequence = [sequence1[0], sequence1[1], sequence2[1]]
            sizedThree.append(newSequence)
            sizedThreeStarting[sequence1[0]].append(newSequence)
            
            ##Setting the global vars
            innerSeq = [sequence1[1]]
            freeAfter = [sequence1[1], sequence2[1]]
            freeFirst = sequence1
            self.helperVariables.oneInnerJourney_rt[sequence1[0]][sequence2[-1]].append({"s": innerSeq, "w": self.computeLt(innerSeq)})
            self.helperVariables.twoInnerJourney_rt[sequence1[0]]["free"].append({"s": freeAfter, "w": self.computeLt(freeAfter)})
            self.helperVariables.twoInnerJourney_rt["free"][sequence2[-1]].append({"s": freeFirst, "w": self.computeLt(freeFirst)})
            self.helperVariables.threeInnerJourney_rt["free"]["free"].append({"s": newSequence, "w": self.computeLt(newSequence)})
    
    print("The monster for sized 4")
    if highest_cmax >= 4:
        sizedFour = []
        for sequence1 in sizedTwo:
            tEndingFirst = sequence1[-1]
            for tStartingSecond in r_t_plain[tEndingFirst]:
                for sequence2 in sizedTwoStarting[tStartingSecond]:
                    newSequence = sequence1 + sequence2
                    sizedFour.append(newSequence)
                    sizedFourStarting[sequence1[0]].append(newSequence)
                    
                    ##Setting the global vars
                    innerSeq = [sequence1[1], sequence2[0]]
                    freeAfter = [sequence1[1]] + sequence2
                    freeFirst = sequence1 + [sequence2[0]]
                    self.helperVariables.twoInnerJourney_rt[sequence1[0]][sequence2[-1]].append({"s": innerSeq, "w": self.computeLt(innerSeq)})
                    self.helperVariables.threeInnerJourney_rt[sequence1[0]]["free"].append({"s": freeAfter, "w": self.computeLt(freeAfter)})
                    self.helperVariables.threeInnerJourney_rt["free"][sequence2[-1]].append({"s": freeFirst, "w": self.computeLt(freeFirst)})
                    self.helperVariables.fourInnerJourney_rt["free"]["free"].append({"s": newSequence, "w": self.computeLt(newSequence)})
            
    print("The monster for sized 5")
    if highest_cmax >= 5:
        sizedFive = []
        for sequence1 in sizedTwo:
            tEndingFirst = sequence1[-1]
            for tStartingSecond in r_t_plain[tEndingFirst]:
                for sequence2 in sizedThreeStarting[tStartingSecond]:
                    newSequence = sequence1 + sequence2
                    #sizedFive.append(newSequence)
                    #sizedFiveStarting[sequence1[0]].append(newSequence)
                    
                    ##Setting the global vars
                    innerSeq = [sequence1[1], sequence2[0], sequence2[1]]
                    freeAfter = [sequence1[1]] + sequence2
                    freeFirst = sequence1 + [sequence2[0], sequence2[1]]
                    self.helperVariables.threeInnerJourney_rt[sequence1[0]][sequence2[-1]].append({"s": innerSeq, "w": self.computeLt(innerSeq)})
                    self.helperVariables.fourInnerJourney_rt[sequence1[0]]["free"].append({"s": freeAfter, "w": self.computeLt(freeAfter)})
                    self.helperVariables.fourInnerJourney_rt["free"][sequence2[-1]].append({"s": freeFirst, "w": self.computeLt(freeFirst)})
                    self.helperVariables.fiveInnerJourney_rt["free"]["free"].append({"s": newSequence, "w": self.computeLt(newSequence)})
            
    print("The monster for sized 6")
    if highest_cmax >= 6:
        sizedSix = []
        for sequence1 in sizedTwo:
            tEndingFirst = sequence1[-1]
            for tStartingSecond in r_t_plain[tEndingFirst]:
                for sequence2 in sizedFourStarting[tStartingSecond]:
                    newSequence = sequence1 + sequence2
                    #sizedSix.append(newSequence)
                    #sizedSixStarting[sequence1[0]].append(newSequence)
                    
                    ##Setting the global vars
                    innerSeq = [sequence1[1], sequence2[0], sequence2[1], sequence2[2]]
                    freeAfter = [sequence1[1]] + sequence2
                    freeFirst = sequence1 + [sequence2[0], sequence2[1], sequence2[2]]
                    self.helperVariables.fourInnerJourney_rt[sequence1[0]][sequence2[-1]].append({"s": innerSeq, "w": self.computeLt(innerSeq)})
                    self.helperVariables.fiveInnerJourney_rt[sequence1[0]]["free"].append({"s": freeAfter, "w": self.computeLt(freeAfter)})
                    self.helperVariables.fiveInnerJourney_rt["free"][sequence2[-1]].append({"s": freeFirst, "w": self.computeLt(freeFirst)})
                    self.helperVariables.sixInnerJourney_rt["free"]["free"].append({"s": newSequence, "w": self.computeLt(newSequence)})

    print("Party over")

    self.helperVariables.oneInnerJourney_rt["free"]["free"] = list(k for k,_ in itertools.groupby(self.helperVariables.oneInnerJourney_rt["free"]["free"]))
    self.helperVariables.twoInnerJourney_rt["free"]["free"] = list(k for k,_ in itertools.groupby(self.helperVariables.twoInnerJourney_rt["free"]["free"]))
    self.helperVariables.threeInnerJourney_rt["free"]["free"] = list(k for k,_ in itertools.groupby(self.helperVariables.threeInnerJourney_rt["free"]["free"]))
    self.helperVariables.fourInnerJourney_rt["free"]["free"] = list(k for k,_ in itertools.groupby(self.helperVariables.fourInnerJourney_rt["free"]["free"]))
    self.helperVariables.fiveInnerJourney_rt["free"]["free"] = list(k for k,_ in itertools.groupby(self.helperVariables.fiveInnerJourney_rt["free"]["free"]))
    self.helperVariables.sixInnerJourney_rt["free"]["free"] = list(k for k,_ in itertools.groupby(self.helperVariables.sixInnerJourney_rt["free"]["free"]))
    for tStart in range(self.nurseModel.T):
        self.helperVariables.oneInnerJourney_rt["free"][tStart] = list(k for k,_ in itertools.groupby(self.helperVariables.oneInnerJourney_rt["free"][tStart]))
        self.helperVariables.oneInnerJourney_rt[tStart]["free"] = list(k for k,_ in itertools.groupby(self.helperVariables.oneInnerJourney_rt[tStart]["free"]))
        self.helperVariables.twoInnerJourney_rt["free"][tStart] = list(k for k,_ in itertools.groupby(self.helperVariables.twoInnerJourney_rt["free"][tStart]))
        self.helperVariables.twoInnerJourney_rt[tStart]["free"] = list(k for k,_ in itertools.groupby(self.helperVariables.twoInnerJourney_rt[tStart]["free"]))
        self.helperVariables.threeInnerJourney_rt["free"][tStart] = list(k for k,_ in itertools.groupby(self.helperVariables.threeInnerJourney_rt["free"][tStart]))
        self.helperVariables.threeInnerJourney_rt[tStart]["free"] = list(k for k,_ in itertools.groupby(self.helperVariables.threeInnerJourney_rt[tStart]["free"]))
        self.helperVariables.fourInnerJourney_rt["free"][tStart] = list(k for k,_ in itertools.groupby(self.helperVariables.fourInnerJourney_rt["free"][tStart]))
        self.helperVariables.fourInnerJourney_rt[tStart]["free"] = list(k for k,_ in itertools.groupby(self.helperVariables.fourInnerJourney_rt[tStart]["free"]))
        for tEnd in range(self.nurseModel.T):
            self.helperVariables.oneInnerJourney_rt[tStart][tEnd] = list(k for k,_ in itertools.groupby(self.helperVariables.oneInnerJourney_rt[tStart][tEnd]))
            self.helperVariables.twoInnerJourney_rt[tStart][tEnd] = list(k for k,_ in itertools.groupby(self.helperVariables.twoInnerJourney_rt[tStart][tEnd]))
            self.helperVariables.threeInnerJourney_rt[tStart][tEnd] = list(k for k,_ in itertools.groupby(self.helperVariables.threeInnerJourney_rt[tStart][tEnd]))
            self.helperVariables.fourInnerJourney_rt[tStart][tEnd] = list(k for k,_ in itertools.groupby(self.helperVariables.fourInnerJourney_rt[tStart][tEnd]))
            
    
def shiftFreeMark(self, shift):
    if shift == -1:
        return "free"
    return shift
def shiftFreeUnMark(self, shift):
    if shift == "free":
        return -1
    return shift

def getOptions(self, nurse, dayStart, dayEnd, size):

    if dayStart - 1 >= 0:
        tStart = self.shiftFreeMark(self.helperVariables.projectedX[dayStart+1])
    else:
        tStart = "free"
    if dayEnd + 1 < self.nurseModel.D: 
        tEnd = self.shiftFreeMark(self.helperVariables.projectedX[dayEnd+1])
    else:
        tEnd = "free"

    allOptions = []
    if size == 1:
        allOptions = self.helperVariables.oneInnerJourney_rt[tStart-1][tEnd+1]
    elif size == 2:
        allOptions = self.helperVariables.twoInnerJourney_rt[tStart-1][tEnd+1]
    elif size == 3:
        allOptions = self.helperVariables.threeInnerJourney_rt[tStart-1][tEnd+1]
    elif size == 4:
        allOptions = self.helperVariables.fourInnerJourney_rt[tStart-1][tEnd+1]
    elif size == 5:
        allOptions = self.helperVariables.fiveInnerJourney_rt[tStart-1][tEnd+1]
    elif size == 6:
        allOptions = self.helperVariables.sixInnerJourney_rt[tStart-1][tEnd+1]

    return allOptions

def verifyWorkload(self, nurse, workLoadOlds, news, bonus:int = 0):
    newWorkLoad = self.helperVariables.workloadCounter[nurse] - workLoadOlds + self.computeLt(news) + bonus
    return newWorkLoad >= self.nurseModel.data.parameters.b_min[nurse] and newWorkLoad <= self.nurseModel.data.parameters.b_max[nurse]

def verifyMaxShifts(self, nurse, olds, news):
    affectedShifts = list(dict.fromkeys(olds+news))

    for shift in affectedShifts:
        if self.nurseModel.data.parameters.m_max[nurse][shift] < self.helperVariables.shiftTypeCounter[nurse][shift] - olds.count(shift) + news.count(shift):
            return False

    return True

def evaluateFO(self, oldObj, newObj, worse:bool = False, better:bool = True, equal:bool = False):

    if better and oldObj > newObj:
        return True
    if worse and oldObj < newObj:
        return True
    if equal and oldObj == newObj:
        return True
    return False
