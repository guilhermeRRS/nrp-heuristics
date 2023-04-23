# coding=utf-8
from chronos import Chronos
from interface import MipInterface
from model import GurobiOptimizedOutput, NurseModel, Solution
from partition import Partition, PartitionHolder, PartitionSize
import gurobipy as gp
from gurobipy import GRB

ORIGIN_RELAX = "ORIGIN_RELAX"

START_ITERATION = "START_ITERATION"
SOLVER_GUROBI_OUTPUT = "SOLVER_GUROBI_OUTPUT"
SOLVER_ITERATION_NO_SOLUTION = "SOLVER_ITERATION_NO_SOLUTION"
SOLVER_ITERATION_NO_TIME = "SOLVER_ITERATION_NO_TIME"

class Relax(MipInterface):

    chronos: Chronos

    def __init__(self, nurseModel: NurseModel, chronos: Chronos):
        super().__init__(nurseModel.model)

        self.nurseModel = nurseModel
        self.chronos = chronos

    def run(self):
        
        success = True

        currentNurse = 0
        while currentNurse < self.nurseModel.I and self.chronos.stillValid() and success:

            success = self.generateNurse(currentNurse)


            currentNurse += 1
        

        return False, self.nurseModel
    
    def generateNurse(self, nurse: int):
        s = False

        

        while self.chronos.stillValid()

        return s