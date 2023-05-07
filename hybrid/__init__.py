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
    worstDays: OneDimInt
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

class Hybrid:

    nurseModel: NurseModel
    chronos: Chronos
    helperVariables: HelperVariables

    from ._utils import generateFromSolution, computeLt, shiftFreeMark, shiftFreeUnMark, getOptions, evaluateFO

    from .rules._forSingle import const_single, math_single, math_single_demand, math_single_preference
    
    from .runs._run_single import run_single, const2_verify
    from .runs._run_focusWorseDays import run_focusWorseDays
    
    from .commits._commit_single import commit_single

    
    def __init__(self, nurseModel: NurseModel, chronos: Chronos):
        self.nurseModel = nurseModel
        self.chronos = chronos
        self.helperVariables = HelperVariables()
        self.penalties = penalties()

    def runNeighbourhoods(self):
        numberFail = 0
        limitRuns = 1000
        nOfSmoves = 0
        
        for i in range(limitRuns):
            s, move = self.run_single(worse = False, better = True, equal = False)
            if s:
                print(move)
                self.commit_single(move)
                nOfSmoves += 1
            else:
                numberFail += 1
            
            if nOfSmoves == 10:
                break
        
        #self.run_focusWorseDays()
        print("output", limitRuns - numberFail, numberFail, limitRuns)
       
    def run(self, startObj):
        m = self.nurseModel.model.m
        self.startObj = startObj
        self.currentObj = startObj
        self.chronos.startCounter("START_SETTING_START")
        self.generateFromSolution()
        input(self.penalties.total)
        self.chronos.stopCounter()
        print("Start working")
        while self.chronos.stillValidRestrict():

            self.runNeighbourhoods()
            break

        ########################################

        ########## HERE WE FINISH THE ALGORITHM IN ORDER TO LATER PRINT, DONT EDIT IT
        ########## THE TIME COST MAY BE REALY SMALL, SO IT IS FIXED A HUGE TIMELIMIT FOR THE SOLVER

        ########################################
        print("-->",self.penalties.total)
        m.setParam("TimeLimit", 43200)
        
        self.chronos.startCounter("START_OPTIMIZE_LAST")
        m.optimize()
        self.chronos.stopCounter()

        gurobiReturn = GurobiOptimizedOutput(m)

        self.chronos.printObj(ORIGIN_SOLVER, SOLVER_GUROBI_OUTPUT, gurobiReturn)

        if gurobiReturn.valid():

            self.nurseModel.solution = Solution().getFromX(self.nurseModel.model.x)
            self.nurseModel.solution = Solution().getFromLb(self.nurseModel.model.x)
            self.nurseModel.solution.printSolution("failed.sol", self.nurseModel.data.sets)
            self.nurseModel.s_solution = True
            return True, self.nurseModel
        
        else:
            self.nurseModel.solution = Solution().getFromLb(self.nurseModel.model.x)
            self.nurseModel.solution.printSolution("failed.sol", self.nurseModel.data.sets)
            self.chronos.printMessage(ORIGIN_SOLVER, SOLVER_ITERATION_NO_SOLUTION, False)
            
        self.chronos.printMessage(ORIGIN_SOLVER, "NOT_ABLE_TO_SAVE", True)
            
        return False, self.nurseModel