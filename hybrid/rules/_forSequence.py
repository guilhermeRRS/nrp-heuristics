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

def math_sequence(self, nurse, dayStart, dayEnd, oldShifts, newShifts):
    penalty = self.penalties.total
    for i in range(len(oldShifts)):
        penalty += self.math_single_preferenceDelta(nurse, dayStart+i, oldShifts[i], newShifts[i])
        penalty += self.math_single_demandDelta(dayStart+i, oldShifts[i], newShifts[i])
    return penalty