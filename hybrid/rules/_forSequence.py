def min_max_possible_workload(self, nurse, oldShiftsWorkLoad):

    b_min = self.nurseModel.data.parameters.b_min[nurse]
    b_max = self.nurseModel.data.parameters.b_max[nurse]

    newWorkload = self.helperVariables.workloadCounter[nurse] - oldShiftsWorkLoad

    return b_min - newWorkload, b_max - newWorkload

def const_sequence(self, nurse, oldShifts, newShifts):

    
    newWorkload = self.helperVariables.workloadCounter[nurse] - oldShifts["w"] + newShifts["w"]

    b_min = self.nurseModel.data.parameters.b_min[nurse]
    b_max = self.nurseModel.data.parameters.b_max[nurse]

    if newWorkload < b_min or newWorkload > b_max:
        return False
    
    affectedShifts = list(dict.fromkeys(newShifts["s"]))
    for affectedShift in affectedShifts:
        if self.helperVariables.shiftTypeCounter[nurse][affectedShift] - oldShifts["s"].count(affectedShift) + newShifts["s"].count(affectedShift) > self.nurseModel.data.parameters.m_max[nurse][affectedShift]:
            return False
    
    return True

def math_demandSingleShift_manyNurses_daySequence(self, dayStart, dayIndex, oldShifts, newShifts, shift):

    penaltyOld = 0
    penaltyNew = 0

    day = dayStart + dayIndex

    numberNurses = self.penalties.numberNurses[day]
    demand = self.nurseModel.data.parameters.u[day]

    w_min = self.nurseModel.data.parameters.w_min[day]
    w_max = self.nurseModel.data.parameters.w_max[day]

    day = dayIndex

    if numberNurses[shift] > demand[shift]:
        penaltyOld -= (numberNurses[shift] - demand[shift])*w_max[shift]
    if numberNurses[shift] < demand[shift]:
        penaltyOld -= (demand[shift] - numberNurses[shift])*w_min[shift]
    
    newNumberOfNurses = numberNurses[shift] - oldShifts[day].count(shift) + newShifts[day].count(shift)
    if newNumberOfNurses > demand[shift]:
        penaltyOld += (newNumberOfNurses - demand[shift])*w_max[shift]
    if newNumberOfNurses < demand[shift]:
        penaltyOld += (demand[shift] - newNumberOfNurses)*w_min[shift]

    #only useful if commit happens right after the math
    self.dayDeltaPenaltyOld_list.append(penaltyOld) 
    self.dayDeltaPenaltyNew_list.append(penaltyNew)

    return penaltyOld + penaltyNew

def math_sequence(self, nurse, dayStart, dayEnd, oldShifts, newShifts):
    penalty = self.penalties.total
    for i in range(len(oldShifts)):
        penalty += self.math_single_preferenceDelta(nurse, dayStart+i, oldShifts[i], newShifts[i])
        penalty += self.math_single_demandDelta(dayStart+i, oldShifts[i], newShifts[i])
    return penalty

def math_manyNurses_daySequence(self, oldShifts, earliestDay, move):
    newShifts = []

    preferenceDelta = 0
    
    for d in range(earliestDay, earliestDay+len(oldShifts)):
        newShifts.append([])
        for i in range(len(move)):
            dayIndex_oldNewShift = d - move[i]["dayStart"]
            if d >= move[i]["dayStart"] and d < move[i]["dayStart"] + move[i]["length"]:
                newShifts[-1].append(move[i]["s"][dayIndex_oldNewShift])
                preferenceDelta += self.math_single_preferenceDelta(move[i]["n"], d, oldShifts[dayIndex_oldNewShift][i], newShifts[dayIndex_oldNewShift][i])
            else:
                newShifts[-1].append(-1)

    self.dayDeltaPenaltyOld_list = [] 
    self.dayDeltaPenaltyNew_list = [] 

    demandDelta = 0
    for d in range(earliestDay, earliestDay+len(oldShifts)):
        day = d - earliestDay
        affectedShifts = list(dict.fromkeys(oldShifts[day] + newShifts[day]))
        for shift in affectedShifts:
            if shift >= 0:
                demandDelta += self.math_demandSingleShift_manyNurses_daySequence(earliestDay, day, oldShifts, newShifts, shift)
                
    return self.penalties.total + demandDelta + preferenceDelta