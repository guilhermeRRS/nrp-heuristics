# coding=utf-8
from chronos import Chronos
from model import NurseModel, Solution, GurobiOptimizedOutput
from typing import List, Dict, NewType
import random
import gurobipy as gp
from gurobipy import GRB

ORIGIN_SOLVER = "ORIGIN_SOLVER"
START_OPTIMIZE = "START_OPTIMIZE"

SOLVER_GUROBI_OUTPUT = "SOLVER_GUROBI_OUTPUT"
SOLVER_ITERATION_NO_SOLUTION = "SOLVER_ITERATION_NO_SOLUTION"
SOLVER_ITERATION_NO_TIME = "SOLVER_ITERATION_NO_TIME"

OneDimInt = NewType("oneDimInt", List[int])
TwoDimInt = NewType("twoDimInt", List[List[int]])
TwoDimVar = NewType("twoDimVar", List[List[gp.Var]])
ThreeDimInt = NewType("threeDimInt", List[List[List[int]]])
ThreeDimVar = NewType("threeDimVar", List[List[List[gp.Var]]])

class penalties:

    numberNurses: TwoDimInt
    demand: int
    preference_total: int

    total: int

class HelperVariables:

    shiftTypeCounter: TwoDimInt
    workloadCounter: OneDimInt
    weekendCounter: TwoDimInt #yes, this is the same as K variable
    projectedX: TwoDimInt

    oneInnerJourney_rt: Dict[int, Dict[int, OneDimInt]]
    twoInnerJourney_rt: Dict[int, Dict[int, TwoDimInt]]

    def __str__(self):
        output = "========================\n"

        output += "shiftTypeCounter: " + str(self.shiftTypeCounter) + "\n"
        output += "workloadCounter: " + str(self.workloadCounter) + "\n"
        output += "weekendCounter: " + str(self.weekendCounter) + "\n"
        output += "projectedX: " + str(self.projectedX) + "\n"

        output += "========================"

        return output


class Hybrid:

    nurseModel: NurseModel
    chronos: Chronos
    helperVariables: HelperVariables

    from ._utils import generateFromSolution, computeLt, shiftFreeMark, shiftFreeUnMark
    from ._runners import run_nurseSingle_daySingle_mustWork

    from ._changesContract import SingleChange

    def __init__(self, nurseModel: NurseModel, chronos: Chronos):
        self.nurseModel = nurseModel
        self.chronos = chronos
        self.helperVariables = HelperVariables()
        self.penalties = penalties()

    def singularDemand(self, day, shift, numberNurses):
        neededNurses = self.nurseModel.data.parameters.u[day][shift]
        dayShiftPenalty = 0
        if numberNurses < neededNurses:
            dayShiftPenalty += (neededNurses - numberNurses)*self.nurseModel.data.parameters.w_min[day][shift]
        elif numberNurses > neededNurses:
            dayShiftPenalty += (numberNurses - neededNurses)*self.nurseModel.data.parameters.w_max[day][shift]
        return dayShiftPenalty

    
    def runNeighbourhoods(self):
        counter = 0
        while self.chronos.stillValidRestrict() and counter < 3:
            s, change = self.run_nurseSingle_daySingle_mustWork(anyObj = False, allowEqual = False)
            if s:
                self.currentObj = change.obj
                change.apply()
            else:
                counter += 1
                
        
    def run(self, startObj):
        m = self.nurseModel.model.m
        self.startObj = startObj
        self.currentObj = startObj
        self.chronos.startCounter("START_SETTING_START")
        self.generateFromSolution()
        self.chronos.stopCounter()
        print("Start working")
        while self.chronos.stillValidRestrict():

            self.runNeighbourhoods()
            break

        ########################################

        ########## HERE WE FINISH THE ALGORITHM IN ORDER TO LATER PRINT, DONT EDIT IT
        ########## THE TIME COST MAY BE REALY SMALL, SO IT IS FIXED A HUGE TIMELIMIT FOR THE SOLVER

        ########################################
        print(self.penalties.total)
        m.setParam("TimeLimit", 43200)
        
        self.chronos.startCounter("START_OPTIMIZE_LAST")
        m.optimize()
        self.chronos.stopCounter()

        gurobiReturn = GurobiOptimizedOutput(m)

        self.chronos.printObj(ORIGIN_SOLVER, SOLVER_GUROBI_OUTPUT, gurobiReturn)

        if gurobiReturn.valid():

            self.nurseModel.solution = Solution().getFromX(self.nurseModel.model.x)
            self.nurseModel.s_solution = True
            return True, self.nurseModel
        
        else:
            self.nurseModel.solution = Solution().getFromLb(self.nurseModel.model.x)
            self.nurseModel.solution.printSolution("failed.sol", self.nurseModel.data.sets)
            self.chronos.printMessage(ORIGIN_SOLVER, SOLVER_ITERATION_NO_SOLUTION, False)
            
        self.chronos.printMessage(ORIGIN_SOLVER, "NOT_ABLE_TO_SAVE", True)
            
        return False, self.nurseModel