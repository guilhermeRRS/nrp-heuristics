# coding=utf-8
from model import NurseModel, Solution
import gurobipy as gp
from gurobipy import GRB

class Solver:

    nurseModel: NurseModel

    def __init__(self, nurseModel: NurseModel):
        self.nurseModel = nurseModel

    def run(self, time: int):
        m = self.nurseModel.model.m
        m.setParam("TimeLimit", time)
        m.optimize()
        self.nurseModel.solution = Solution().getFromX(self.nurseModel.model.x)
        self.nurseModel.s_solution = True
        print(Solution().getFromX(self.nurseModel.model.x))
        return self.nurseModel