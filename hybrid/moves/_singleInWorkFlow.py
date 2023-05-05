import random

def move_singleInWorkflow(self, nurse, day):
    currentDay = self.helperVariables.projectedX[nurse][day]
    if currentDay == -1:
        #print("SINGLE -> BUT FREE")
        return False, -1, -1
    else:
        if day == 0:
            dayBefore = "free"
        else:
            dayBefore = self.shiftFreeMark(self.helperVariables.projectedX[nurse][day-1])
        if day == self.nurseModel.D - 1:
            dayAfter = "free"
        else:
            dayAfter = self.shiftFreeMark(self.helperVariables.projectedX[nurse][day+1])
        
        options = self.helperVariables.parallelR_t[dayBefore][dayAfter]
        

        if len(options) - 1 == 0:
            #print("SINGLE -> BUT NONE")
            return False, -1, -1
        
        while True:
            newShift = random.choice(options)
            if newShift != currentDay:

                if self.const_singleInWorkflow(nurse, day, currentDay, newShift):
                    return True, currentDay, newShift
                #print("SINGLE -> BUT INFAC")
                return False, -1, -1
            
def const_singleInWorkflow(self, nurse, day, oldShift, newShift):

    if self.helperVariables.shiftTypeCounter[nurse][newShift] + 1 <= self.nurseModel.data.parameters.m_max[nurse][newShift]:
        workLoad = self.helperVariables.workloadCounter[nurse] - self.nurseModel.data.parameters.l_t[oldShift] + - self.nurseModel.data.parameters.l_t[newShift]
        if workLoad >= self.nurseModel.data.parameters.b_min[nurse] and workLoad <= self.nurseModel.data.parameters.b_max[nurse]:
            return True
    return False

def math_singleInWorkflow(self, nurse, day, oldShift, newShift):

    preferenceComponent = self.penalties.preference_total
    preferenceComponent -= self.nurseModel.data.parameters.p[nurse][day][oldShift]
    preferenceComponent += self.nurseModel.data.parameters.q[nurse][day][oldShift]
    preferenceComponent -= self.nurseModel.data.parameters.q[nurse][day][newShift]
    preferenceComponent += self.nurseModel.data.parameters.p[nurse][day][newShift]

    demandComponent = self.penalties.demand
    demandComponent -= self.singularDemand(day, oldShift, self.penalties.numberNurses[day][oldShift])
    demandComponent += self.singularDemand(day, oldShift, self.penalties.numberNurses[day][oldShift]-1)
    demandComponent -= self.singularDemand(day, newShift, self.penalties.numberNurses[day][newShift])
    demandComponent += self.singularDemand(day, newShift, self.penalties.numberNurses[day][newShift]+1)

    return preferenceComponent, demandComponent, preferenceComponent + demandComponent

def apply_singleInWorkflow(self, nurse, day, oldShift, newShift, preferenceComponent, demandComponent, totalPenalty):
    self.penalties.numberNurses[day][oldShift] -= 1
    self.penalties.numberNurses[day][newShift] += 1

    self.penalties.demand = demandComponent
    self.penalties.preference_total = preferenceComponent
    self.penalties.total = totalPenalty

    self.helperVariables.shiftTypeCounter[nurse][oldShift] -= 1
    self.helperVariables.shiftTypeCounter[nurse][newShift] += 1

    self.helperVariables.workloadCounter[nurse] -= self.nurseModel.data.parameters.l_t[oldShift]
    self.helperVariables.workloadCounter[nurse] += self.nurseModel.data.parameters.l_t[newShift]
        
    self.helperVariables.projectedX[nurse][day] = newShift

    self.nurseModel.model.x[nurse][day][oldShift].lb = 0
    self.nurseModel.model.x[nurse][day][oldShift].ub = 0
    self.nurseModel.model.x[nurse][day][newShift].lb = 1
    self.nurseModel.model.x[nurse][day][newShift].ub = 1