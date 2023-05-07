import random

from model import GurobiOptimizedOutput

def run_focusWorseDays(self, numberOfIters:int = 10):
    for z in range(numberOfIters):
        allDays = list(range(self.nurseModel.D))

        days = random.choices(allDays, weights=self.penalties.worstDays, k = int(self.nurseModel.D*0.25))
        days = list(dict.fromkeys(days))
        
        for day in days:
            for i in range(self.nurseModel.I):
                for t in range(self.nurseModel.T):
                    self.nurseModel.model.x[i][day][t].Start = 1 if self.helperVariables.projectedX[i][day] == t else 0
                    self.nurseModel.model.x[i][day][t].lb = 0
                    self.nurseModel.model.x[i][day][t].ub = 1

        if self.chronos.stillValidRestrict():
            print("!", self.penalties.total)
            self.nurseModel.model.m.setParam("TimeLimit", self.chronos.timeLeft())
            self.nurseModel.model.m.setParam("BestObjStop", self.penalties.total - 100)
            self.nurseModel.model.m.update()
            self.nurseModel.model.m.optimize()
            input("@")

            gurobiReturn = GurobiOptimizedOutput(self.nurseModel.model.m)

            self.chronos.printObj("WORST", "OUTPUT", gurobiReturn)

            if gurobiReturn.valid():
                for i in range(self.nurseModel.I):
                    for t in range(self.nurseModel.T):
                        newValue = self.nurseModel.model.x[i][day][t].x
                        self.nurseModel.model.x[i][day][t].lb = newValue
                        self.nurseModel.model.x[i][day][t].ub = newValue
            raise Exception("Needs to couple with the rest of the code")
        else:
            break