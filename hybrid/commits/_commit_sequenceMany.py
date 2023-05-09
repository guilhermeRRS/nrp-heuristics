def commit_sequenceMany(self, move):
    newShifts = move["s"]

    #####here, needs to calculate

    self.penalties.demand = self.math_single_demand(day, oldShift, newShift)
    self.penalties.preference_total = self.math_single_preference(nurse, day, oldShift, newShift)

    self.penalties.total = self.penalties.demand + self.penalties.preference_total

    self.penalties.worstDaysShifts[day][oldShift] += self.dayDeltaPenaltyOld
    self.penalties.worstDaysShifts[day][newShift] += self.dayDeltaPenaltyNew
    self.penalties.worstDays[day] += self.dayDeltaPenaltyNew + self.dayDeltaPenaltyOld
    
    self.nurseModel.model.x[nurse][day][oldShift].lb = 0
    self.nurseModel.model.x[nurse][day][oldShift].ub = 0
    self.nurseModel.model.x[nurse][day][newShift].lb = 1
    self.nurseModel.model.x[nurse][day][newShift].ub = 1

    self.helperVariables.projectedX[nurse][day] = newShift

    self.helperVariables.shiftTypeCounter[nurse][oldShift] -= 1
    self.helperVariables.shiftTypeCounter[nurse][newShift] += 1

    self.helperVariables.workloadCounter[nurse] += (self.nurseModel.data.parameters.l_t[newShift] - self.nurseModel.data.parameters.l_t[oldShift])

    self.penalties.numberNurses[day][oldShift] -= 1
    self.penalties.numberNurses[day][newShift] += 1