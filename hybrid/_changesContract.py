import random

class SingleChange():

    def math_fo(self, currentShift, shift):
        nurse = self.nurse
        day = self.day
        newObj = self.hybrid.penalties.preference_total
        newObj -= (self.hybrid.nurseModel.data.parameters.p[nurse][day][currentShift] - self.hybrid.nurseModel.data.parameters.q[nurse][day][currentShift])
        newObj += (self.hybrid.nurseModel.data.parameters.p[nurse][day][shift] - self.hybrid.nurseModel.data.parameters.q[nurse][day][shift])
        self.preference_total = newObj
        newObj += self.penaltyDemand_single(day, currentShift, shift)
        return newObj

    def __init__(self, hybrid, nurse, day, anyObj:bool = False, allowEqual:bool = False): #order: anyObj then allowEqual then onlyBetter (not needed to create this var)

        self.nurse = nurse
        self.day = day

        self.valid = False
        self.hybrid = hybrid

        shiftBefore = "free"
        if day - 1 >= 0:
            shiftBefore = hybrid.shiftFreeMark(hybrid.helperVariables.projectedX[nurse][day - 1])
        shiftAfter = "free"
        if day + 1 < hybrid.nurseModel.D:
            shiftAfter = hybrid.shiftFreeMark(hybrid.helperVariables.projectedX[nurse][day + 1])

        currentShift = hybrid.helperVariables.projectedX[nurse][day]

        allOptions = hybrid.helperVariables.oneInnerJourney_rt[shiftBefore][shiftAfter]

        asFreeWorkLoad = hybrid.helperVariables.workloadCounter[nurse] - hybrid.nurseModel.data.parameters.l_t[currentShift]

        options = []
        b_min = hybrid.nurseModel.data.parameters.b_min[nurse]
        b_max = hybrid.nurseModel.data.parameters.b_max[nurse]
                
        for opt in allOptions:
            newWorkLoad = asFreeWorkLoad + opt["w"]
            if newWorkLoad >= b_min and newWorkLoad <= b_max:
                shift = opt["s"][0]
                if hybrid.helperVariables.shiftTypeCounter[nurse][shift] + 1 <= hybrid.nurseModel.data.parameters.m_max[nurse][shift]:
                    shift = opt["s"][0]
                    opt["o"] = self.math_fo(currentShift, shift)
                    options.append(opt)

        if len(options) > 0:
            if anyObj:
                self.change = random.choice(options)
                self.obj = options["o"]
                self.valid = True
            else:
                validOptions = []
                if allowEqual:
                    for opt in options:
                        if opt["o"] <= hybrid.penalties.total:
                            validOptions.append(opt)
                else:
                    for opt in options:
                        shift = opt["s"][0]
                        if opt["o"] < hybrid.penalties.total:
                            validOptions.append(opt)
                        else:
                            print(opt["o"], hybrid.penalties.total)

                print(len(options), len(validOptions))

                if len(validOptions) > 0:
                    self.change = random.choice(validOptions)
                    self.obj = self.change["o"]
                    self.valid = True

    def penaltyDemand_single(self, day, oldShift, newShift):
        oldNumber = self.hybrid.penalties.numberNurses[day][oldShift]
        oldDemand = self.hybrid.nurseModel.data.parameters.u[day][oldShift]

        newNumber = self.hybrid.penalties.numberNurses[day][newShift]
        newDemand = self.hybrid.nurseModel.data.parameters.u[day][newShift]
        
        penalty = self.hybrid.penalties.demand
        if oldNumber > oldDemand:
            penalty -= (oldNumber - oldDemand)*self.hybrid.nurseModel.data.parameters.w_max[day][oldShift]
        if oldNumber < oldDemand:
            penalty -= (oldDemand - oldNumber)*self.hybrid.nurseModel.data.parameters.w_min[day][oldShift]
        
        if oldNumber-1 > oldDemand:
            penalty += (oldNumber-1 - oldDemand)*self.hybrid.nurseModel.data.parameters.w_max[day][oldShift]
        if oldNumber < oldDemand:
            penalty += (oldDemand - oldNumber-1)*self.hybrid.nurseModel.data.parameters.w_min[day][oldShift]


        if newNumber > newDemand:
            penalty -= (newNumber - newDemand)*self.hybrid.nurseModel.data.parameters.w_max[day][newShift]
        if newNumber < newDemand:
            penalty -= (newDemand - newNumber)*self.hybrid.nurseModel.data.parameters.w_min[day][newShift]
            
        if newNumber+1 > newDemand:
            penalty -= (newNumber+1 - newDemand)*self.hybrid.nurseModel.data.parameters.w_max[day][newShift]
        if newNumber+1 < newDemand:
            penalty -= (newDemand - newNumber+1)*self.hybrid.nurseModel.data.parameters.w_min[day][newShift]

        self.demand = penalty
        return penalty
    
    def apply(self):
        if self.valid:
            
            self.hybrid.penalties.preference_total = self.preference_total
            self.hybrid.penalties.demand = self.demand

            self.hybrid.penalties.numberNurses[]

        else:
            raise Exception("There is no movie to allow")