def math_manyNurses_singleDay_preference(self, penalty, nurse, day, oldShift, newShift):

    q = self.nurseModel.data.parameters.q[nurse][day]
    p = self.nurseModel.data.parameters.q[nurse][day]

    penalty -= (p[oldShift] - q[oldShift])
    penalty += (p[newShift] - q[newShift])

    return penalty

def math_manyNurses_singleDay_demand(self, day, oldShifts, newShifts):

    penalty = self.penalties.demand

    numberNurses = self.penalties.numberNurses[day]
    demand = self.nurseModel.data.parameters.u[day]

    w_min = self.nurseModel.data.parameters.w_min[day]
    w_max = self.nurseModel.data.parameters.w_max[day]

    affectedShifts = list(dict.fromkeys(oldShifts + newShifts))

    for affectedShift in affectedShifts:

        if numberNurses[affectedShift] > demand[affectedShift]:
            penalty -= (numberNurses[affectedShift] - demand[affectedShift])*w_max[affectedShift]
        if numberNurses[affectedShift] < demand[affectedShift]:
            penalty -= (demand[affectedShift] - numberNurses[affectedShift])*w_min[affectedShift]
            
        newNumberOfNurses = numberNurses[affectedShift] - oldShifts.count(affectedShift) + newShifts.count(affectedShift)
        if  newNumberOfNurses > demand[affectedShift]:
            penalty += (newNumberOfNurses - demand[affectedShift])*w_max[affectedShift]
        if newNumberOfNurses < demand[affectedShift]:
            penalty += (demand[affectedShift] - newNumberOfNurses)*w_min[affectedShift]

    return penalty


def math_manyNurses_singleDay(self, numberOfNurses, nurses, day, oldShifts, newShifts):

    penalty_preference = self.penalties.preference_total
    for i in range(numberOfNurses):
        penalty_preference += self.math_manyNurses_singleDay_preference(penalty_preference, nurses[i], day, oldShifts[i], newShifts[i])
    
    return penalty_preference + self.math_manyNurses_singleDay_demand(day, oldShifts, newShifts)