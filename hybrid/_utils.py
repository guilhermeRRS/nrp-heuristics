def generateFromSolution(self):
    self.helperVariables.shiftTypeCounter = []
    self.helperVariables.workloadCounter = []
    self.helperVariables.weekendCounter = []
    self.helperVariables.projectedX = []

    self.penalties.preference_total = 0
    
    self.penalties.numberNurses = []
    for d in range(self.nurseModel.D):
        self.penalties.numberNurses.append([])
        for t in range(self.nurseModel.T):
            self.penalties.numberNurses[-1].append(0)

    for i in range(self.nurseModel.I):
        self.helperVariables.shiftTypeCounter.append([])
        self.helperVariables.workloadCounter.append(0)
        self.helperVariables.weekendCounter.append([])
        self.helperVariables.projectedX.append([])

        for d in range(self.nurseModel.D):
            self.helperVariables.projectedX[-1].append(-1)
            for t in range(self.nurseModel.T):
                self.penalties.preference_total += self.nurseModel.data.parameters.p[i][d][t]*self.nurseModel.solution.solution[i][d][t]+self.nurseModel.data.parameters.q[i][d][t]*(1 - self.nurseModel.solution.solution[i][d][t])
        for t in range(self.nurseModel.T):
            self.helperVariables.shiftTypeCounter[-1].append(0)
            for d in range(self.nurseModel.D):
                self.nurseModel.model.x[i][d][t].ub = self.nurseModel.solution.solution[i][d][t]
                self.nurseModel.model.x[i][d][t].lb = self.nurseModel.solution.solution[i][d][t]

                if self.nurseModel.solution.solution[i][d][t] >= 0.5:
                    self.helperVariables.shiftTypeCounter[-1][-1] += 1
                    self.helperVariables.workloadCounter[-1] += self.nurseModel.data.parameters.l_t[t]
                    self.helperVariables.projectedX[-1][d] = t
                    self.penalties.numberNurses[d][t] += 1

        for w in range(self.nurseModel.W):
            self.helperVariables.weekendCounter[-1].append(1 if (self.helperVariables.projectedX[-1][7*w+5] + self.helperVariables.projectedX[-1][7*w+6]) > 0.5 else 0)
    
    self.penalties.demand = 0
    for d in range(self.nurseModel.D):
        for t in range(self.nurseModel.T):
            numberNurses = self.penalties.numberNurses[d][t]
            neededNurses = self.nurseModel.data.parameters.u[d][t]
            if numberNurses < neededNurses:
                self.penalties.demand += (neededNurses - numberNurses)*self.nurseModel.data.parameters.w_min[d][t]
            elif numberNurses > neededNurses:
                self.penalties.demand += (numberNurses - neededNurses)*self.nurseModel.data.parameters.w_max[d][t]

    self.penalties.total = self.penalties.demand + self.penalties.preference_total

    r_t_plain = []
    self.helperVariables.parallelR_t = {"free": {"free": []}}
    for t in range(self.nurseModel.T):
        
        r_t_plain.append([i for i, x in enumerate(self.nurseModel.data.sets.R_t[t]) if x == 0])

        self.helperVariables.parallelR_t["free"]["free"].append(t)
        self.helperVariables.parallelR_t["free"][t] = []
        self.helperVariables.parallelR_t[t] = {"free": []}
        self.helperVariables.parallelR_t[t]["free"] = r_t_plain[-1]

        for t2 in range(self.nurseModel.T):
            self.helperVariables.parallelR_t[t][t2] = []

    for tb in range(self.nurseModel.T):
        for tc in r_t_plain[tb]:
            self.helperVariables.parallelR_t["free"][tc].append(tb)
            for ta in (r_t_plain[tc]):
                self.helperVariables.parallelR_t[tb][ta].append(tc)
    
def shiftFreeMark(self, shift):
    if shift == -1:
        return "free"
    return shift
def shiftFreeUnMark(self, shift):
    if shift == "free":
        return -1
    return shift
