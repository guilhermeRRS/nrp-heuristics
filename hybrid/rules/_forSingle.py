def const_single(self, nurse, oldShift, newShift):

    l_t = self.nurseModel.data.parameters.l_t

    newWorkload = self.helperVariables.workloadCounter[nurse] - l_t[oldShift] + l_t[newShift]

    b_min = self.nurseModel.data.parameters.b_min[nurse]
    b_max = self.nurseModel.data.parameters.b_max[nurse]

    if newWorkload < b_min or newWorkload > b_max:
        return False
    
    if self.helperVariables.shiftTypeCounter[nurse][newShift] + 1 > self.nurseModel.data.parameters.m_max[nurse][newShift]:
        return False
    
    return True

def math_single_preference(self, nurse, day, oldShift, newShift):

    penalty = self.penalties.preference_total

    q = self.nurseModel.data.parameters.q[nurse][day]
    p = self.nurseModel.data.parameters.q[nurse][day]

    penalty -= (p[oldShift] - q[oldShift])
    penalty += (p[newShift] - q[newShift])

    return penalty

def math_single_demand(self, day, oldShift, newShift):

    penalty = self.penalties.demand

    numberNurses = self.penalties.numberNurses[day]
    demand = self.nurseModel.data.parameters.u[day]

    w_min = self.nurseModel.data.parameters.w_min[day]
    w_max = self.nurseModel.data.parameters.w_max[day]

    if numberNurses[oldShift] > demand[oldShift]:
        penalty -= (numberNurses[oldShift] - demand[oldShift])*w_max[oldShift]
    if numberNurses[oldShift] < demand[oldShift]:
        penalty -= (demand[oldShift] - numberNurses[oldShift])*w_min[oldShift]
    if numberNurses[newShift] > demand[newShift]:
        penalty -= (numberNurses[newShift] - demand[newShift])*w_max[newShift]
    if numberNurses[newShift] < demand[newShift]:
        penalty -= (demand[newShift] - numberNurses[newShift])*w_min[newShift]
        
    if numberNurses[oldShift] - 1 > demand[oldShift]:
        penalty += (numberNurses[oldShift] - 1 - demand[oldShift])*w_max[oldShift]
    if numberNurses[oldShift] - 1 < demand[oldShift]:
        penalty += (demand[oldShift] - numberNurses[oldShift] + 1)*w_min[oldShift]
    if numberNurses[newShift] + 1> demand[newShift]:
        penalty += (numberNurses[newShift] + 1 - demand[newShift])*w_max[newShift]
    if numberNurses[newShift] + 1 < demand[newShift]:
        penalty += (demand[newShift] - numberNurses[newShift] - 1)*w_min[newShift]

    return penalty


def math_single(self, nurse, day, oldShift, newShift):
    
    return self.math_single_preference(nurse, day, oldShift, newShift) + self.math_single_demand(day, oldShift, newShift)