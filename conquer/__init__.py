# coding=utf-8
from chronos import Chronos
from interface import MipInterface
from model import GurobiOptimizedOutput, NurseModel, Solution
import math
import gurobipy as gp
from gurobipy import GRB

ORIGIN_RELAX = "ORIGIN_RELAX"

START_ITERATION = "START_ITERATION"
SOLVER_GUROBI_OUTPUT = "SOLVER_GUROBI_OUTPUT"
SOLVER_ITERATION_NO_SOLUTION = "SOLVER_ITERATION_NO_SOLUTION"
SOLVER_ITERATION_NO_TIME = "SOLVER_ITERATION_NO_TIME"

class Conquer(MipInterface):

    from ._utils import get_extremeShifts
    from ._heuristicsSetters import setDays, setShifts
    from ._createModels import create_days_model, create_shift_model

    chronos: Chronos

    def __init__(self, nurseModel: NurseModel, chronos: Chronos):
        super().__init__(nurseModel.model)

        self.nurseModel = nurseModel
        self.chronos = chronos

    historyOfDaySchedules = []

    def run(self):
        
        success = True
        m = self.nurseModel.model.m

        self.historyOfDaySchedules = []

        currentNurse = 0
        tries = 0
        while currentNurse < self.nurseModel.I and self.chronos.stillValidRestrict() and success:

            success, triesNurse = self.generateNurse(currentNurse)
            currentNurse += 1
            tries += triesNurse
        input(tries)
            
        if self.chronos.stillValidRestrict() and success:
            
            m.setParam("TimeLimit", self.chronos.timeLeft())
            m.setParam("Solutionlimit", 1)
            
            m.optimize()

            gurobiReturn = GurobiOptimizedOutput(m)

            if gurobiReturn.valid() and currentNurse == self.nurseModel.I:

                self.nurseModel.solution = Solution().getFromX(self.nurseModel.model.x)
                self.nurseModel.s_solution = True
                return True, self.nurseModel

        return False, self.nurseModel
        
    def generateNurse(self, currentNurse):

        solution = []
        success = False
        print(currentNurse)
        shortestShiftSize, longestShiftSize = self.get_extremeShifts(currentNurse)

        days_model, dm_x = self.create_days_model(currentNurse, self.nurseModel.data.sets, self.nurseModel.data.parameters)
        days_model.setParam('Solutionlimit', 1)
        days_model.setParam('OutputFlag', 0)

        shift_model, sm_x = self.create_shift_model(currentNurse, self.nurseModel.data.sets, self.nurseModel.data.parameters)
        shift_model.setParam('Solutionlimit', 1)
        shift_model.setParam('OutputFlag', 0)
        
        minimumNumberOfDays = math.ceil(self.nurseModel.data.parameters.b_min[currentNurse]/longestShiftSize)
        maximumNumberOfDays = math.floor(self.nurseModel.data.parameters.b_max[currentNurse]/shortestShiftSize)
        
        zero_minimumNumberOfDays = minimumNumberOfDays
        zero_maximumNumberOfDays = maximumNumberOfDays

        minimumNumberOfDays = maximumNumberOfDays#min(math.floor(1.1*minimumNumberOfDays), zero_maximumNumberOfDays)
        #maximumNumberOfDays = min(math.floor(0.9*maximumNumberOfDays), zero_minimumNumberOfDays)

        tries = 0
        while self.chronos.stillValidRestrict() and not success:
            tries += 1
            days_model.setParam("Timelimit", self.chronos.timeLeft())
            numberOfDays = self.setDays(days_model, dm_x, minimumNumberOfDays, maximumNumberOfDays)
            
            if numberOfDays > -1 and self.chronos.stillValidRestrict():
                days_model.setParam("Timelimit", self.chronos.timeLeft())
                numberOfHours = self.setShifts(shift_model, sm_x, dm_x)
				
                if numberOfHours > -1:
                    success = True
                    for d in self.nurseModel.data.sets.D:
                        for t in range(len(self.nurseModel.data.sets.T)):
                            self.nurseModel.model.x[currentNurse][d][t].lb = sm_x[d][t].x
                            self.nurseModel.model.x[currentNurse][d][t].ub = sm_x[d][t].x
                    break

                else:
                    if numberOfHours < self.nurseModel.data.parameters.b_min[currentNurse]:
                        minimumNumberOfDays += 0.25
                    else:
                        maximumNumberOfDays += 0.25

            else:
                minimumNumberOfDays = max(zero_minimumNumberOfDays, minimumNumberOfDays-1)
                maximumNumberOfDays = min(zero_maximumNumberOfDays, maximumNumberOfDays+1)
        print(tries)
        return success, tries