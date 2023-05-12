import random

from model import GurobiOptimizedOutput


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

def run_seqFromModel(self, rangeOfSequences:int, numberOfTries:int , worse:bool = False, better:bool = False, equal:bool = False): #this is random

    nurse = random.randint(0, self.nurseModel.I-1)
    day = random.choice(self.helperVariables.workingDays[nurse])
    
    x = self.parallelModels[nurse]["x"]
    m = self.parallelModels[nurse]["m"]

    restrictions = []
    workingDays = self.helperVariables.workingDays[nurse]
    freeDays = [i for i, x in enumerate(self.helperVariables.projectedX[nurse]) if x < 0]
    
    restrictions.append(m.addConstr(sum((1 - x[d][t]) for t in range(self.nurseModel.T) for d in workingDays) + sum(x[d][t] for t in range(self.nurseModel.T) for d in freeDays) >= 1))

    dayStart, dayEnd = self.getRangeRewrite(nurse, day, rangeOfSequences)
    for d in range(self.nurseModel.D):
        if d < dayStart or d > dayEnd:
            for t in range(self.nurseModel.T):
                if t == self.helperVariables.projectedX[nurse][d]:
                    x[d][t].lb = 1
                    x[d][t].ub = 1
                else:
                    x[d][t].lb = 0
                    x[d][t].ub = 0
        else:
            for t in range(self.nurseModel.T):
                x[d][t].lb = 0
                x[d][t].ub = 1

    tries = 0
    while tries < numberOfTries and self.chronos.stillValidRestrict():

        m.setParam("TimeLimit", self.chronos.timeLeft())
            
        self.chronos.startCounter(f"Internal optinization number {tries}")
        m.optimize()
        self.chronos.stopCounter()

        gurobiReturn = GurobiOptimizedOutput(m)

        self.chronos.printObj("SEQ_FROM_MODEL", "SOLVER_GUROBI_OUTPUT", gurobiReturn)

        if gurobiReturn.valid():
            newX = []
            for d in range(dayStart, dayEnd+1):
                newX.append(-1)
                for t in range(self.nurseModel.T):
                    if x[d][t].x >= 0.5:
                        newX[-1] = t
                        break
                    
            newObj = self.math_sequence(nurse, dayStart, dayEnd, self.helperVariables.projectedX[nurse][dayStart:(dayEnd+1)], newX)
            if self.evaluateFO(self.penalties.total, newObj, worse, better, equal):
                for restriction in restrictions:
                    m.remove(restriction)
                return True, {"n": nurse, "d": dayStart, "s": newX}
            else:
                #here the restriction may be softer, it means, the day squence may be equal, but shifts must change
                workingDays = []
                freeDays = []
                for d in range(self.nurseModel.D):
                    for t in range(self.nurseModel.T):
                        if x[d][t].x >= 0.5:
                            workingDays.append(d)
                            break
                    if not (d in workingDays):
                        freeDays.append(d)
                        restrictions.append(m.addConstr(sum((1 - x[d][t]) for t in range(self.nurseModel.T) for d in workingDays) + sum(x[d][t] for t in range(self.nurseModel.T) for d in freeDays) >= 1))

        else:
            for restriction in restrictions:
                m.remove(restriction)
            return False, None

        tries += 1
    for restriction in restrictions:
        m.remove(restriction)
    return False, None

def run_seqFromModel_fixed(self, nurse:int, day:int, rangeOfSequences:int): #this is random

    x = self.parallelModels[nurse]["x"]
    m = self.parallelModels[nurse]["m"]

    restrictions = []
    workingDays = self.helperVariables.workingDays[nurse]
    freeDays = [i for i, x in enumerate(self.helperVariables.projectedX[nurse]) if x < 0]
    
    restrictions.append(m.addConstr(sum((1 - x[d][t]) for t in range(self.nurseModel.T) for d in workingDays) + sum(x[d][t] for t in range(self.nurseModel.T) for d in freeDays) >= 1))

    dayStart, dayEnd = self.getRangeRewrite(nurse, day, rangeOfSequences)
    for d in range(self.nurseModel.D):
        if d < dayStart or d > dayEnd:
            for t in range(self.nurseModel.T):
                if t == self.helperVariables.projectedX[nurse][d]:
                    x[d][t].lb = 1
                    x[d][t].ub = 1
                else:
                    x[d][t].lb = 0
                    x[d][t].ub = 0
        else:
            for t in range(self.nurseModel.T):
                x[d][t].lb = 0
                x[d][t].ub = 1

    if self.chronos.stillValidRestrict():

        m.setParam("TimeLimit", self.chronos.timeLeft())
            
        self.chronos.startCounter(f"Internal optinization")
        m.optimize()
        self.chronos.stopCounter()

        gurobiReturn = GurobiOptimizedOutput(m)

        self.chronos.printObj("SEQ_FROM_MODEL", "SOLVER_GUROBI_OUTPUT", gurobiReturn)

        if gurobiReturn.valid():
            newX = []
            for d in range(dayStart, dayEnd+1):
                newX.append(-1)
                for t in range(self.nurseModel.T):
                    if x[d][t].x >= 0.5:
                        newX[-1] = t
                        break
            for restriction in restrictions:
                m.remove(restriction)  
            return True, {"n": nurse, "d": dayStart, "s": newX}
            
        else:
            for restriction in restrictions:
                m.remove(restriction)  
            return False, None
        
    for restriction in restrictions:
        m.remove(restriction)  
    return False, None