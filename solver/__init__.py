# coding=utf-8
from chronos import Chronos
from model import NurseModel, Solution, GurobiOptimizedOutput
import gurobipy as gp
from gurobipy import GRB

class Solver:

    nurseModel: NurseModel
    chronos: Chronos

    def __init__(self, nurseModel: NurseModel, chronos: Chronos):
        self.nurseModel = nurseModel
        self.chronos = chronos
        self.chronos.origin = "SOLVER"

    def run(self):
        m = self.nurseModel.model.m
        timeLeft = self.chronos.timeLeft()
        if timeLeft > 0:
            
            m.setParam("TimeLimit", timeLeft)
            
            self.chronos.startCounter("START OPTIMIZE")
            m.optimize()
            self.chronos.stopCounter()

            if GurobiOptimizedOutput(m.Status, m.SolCount).valid():

                self.nurseModel.solution = Solution().getFromX(self.nurseModel.model.x)
                self.nurseModel.s_solution = True
                return True, self.nurseModel
            
        return False, self.nurseModel