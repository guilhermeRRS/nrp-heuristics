def math_manyInWorkflow(self, nurses, day, oldShifts, newShifts):

    preferenceComponent = self.penalties.preference_total
    for i in range(len(nurses)):
        preferenceComponent -= self.nurseModel.data.parameters.p[nurses[i]][day][oldShifts[i]]
        preferenceComponent += self.nurseModel.data.parameters.q[nurses[i]][day][oldShifts[i]]
        preferenceComponent -= self.nurseModel.data.parameters.q[nurses[i]][day][newShifts[i]]
        preferenceComponent += self.nurseModel.data.parameters.p[nurses[i]][day][newShifts[i]]

    affected_oldShifts = list(dict.fromkeys(oldShifts))
    affected_newShifts = list(dict.fromkeys(newShifts))

    demandComponent = self.penalties.demand
    
    for shift in affected_oldShifts:
        demandComponent -= self.singularDemand(day, shift, self.penalties.numberNurses[day][shift])
        demandComponent += self.singularDemand(day, shift, self.penalties.numberNurses[day][shift]-oldShifts.count(shift))

    for shift in affected_newShifts:
        demandComponent -= self.singularDemand(day, shift, self.penalties.numberNurses[day][shift])
        demandComponent += self.singularDemand(day, shift, self.penalties.numberNurses[day][shift]+newShifts.count(shift))

    return preferenceComponent, demandComponent, preferenceComponent + demandComponent

def apply_manyInWorkflow(self, nurses, day, oldShifts, newShifts, preferenceComponent, demandComponent, totalPenalty):
    
    self.penalties.demand = demandComponent
    self.penalties.preference_total = preferenceComponent
    self.penalties.total = totalPenalty

    for i in range(len(nurses)):
        nurse = nurses[i]
        oldShift = oldShifts[i]
        newShift = newShifts[i]
        self.penalties.numberNurses[day][oldShift] -= 1
        self.penalties.numberNurses[day][newShift] += 1


        self.helperVariables.shiftTypeCounter[nurse][oldShift] -= 1
        self.helperVariables.shiftTypeCounter[nurse][newShift] += 1

        self.helperVariables.workloadCounter[nurse] -= self.nurseModel.data.parameters.l_t[oldShift]
        self.helperVariables.workloadCounter[nurse] += self.nurseModel.data.parameters.l_t[newShift]
            
        self.helperVariables.projectedX[nurse][day] = newShift

        self.nurseModel.model.x[nurse][day][oldShift].lb = 0
        self.nurseModel.model.x[nurse][day][oldShift].ub = 0
        self.nurseModel.model.x[nurse][day][newShift].lb = 1
        self.nurseModel.model.x[nurse][day][newShift].ub = 1