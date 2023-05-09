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

    from .rules._forSingle import const_single, math_single, math_single_demand, math_single_preference, math_single_demandDelta, math_single_preferenceDelta
    from .rules._forSequence import const_sequence, math_sequence, math_manyNurses_daySequence, math_demandSingleShift_manyNurses_daySequence
    
    from .runs._run_single import run_single, const2_verify
    from .runs._run_sequence import run_sequence, getSequenceWorkMarks, getOptions, run_sequence_fixed
    from .runs._run_sequenceMany import run_sequenceMany
    #from .runs._run_focusWorseDays import run_focusWorseDays
    
    from .commits._commit_single import commit_single
    from .commits._commit_sequence import commit_sequence
    from .commits._commit_sequenceMany import commit_sequenceMany

    
    def __init__(self, nurseModel: NurseModel, chronos: Chronos):
        self.nurseModel = nurseModel
        self.chronos = chronos
        self.helperVariables = HelperVariables()
        self.penalties = penalties()

    def runNeighbourhoods(self):
        numberFail = 0
        limitRuns = 2000
        nOfSmoves = 0
        numberOfNurses = 15
        maxIters = numberOfNurses*self.nurseModel.T*self.highest_cmax
        
        for i in range(limitRuns):
            if i % 100 == 0:
                print("===============",i)
                input()
            s, move = self.run_sequenceMany(numberOfNurses = numberOfNurses, maxInsideCombinationOf = maxIters, worse = False, better = True, equal = False)
            if s:
                self.commit_sequenceMany(move)
                nOfSmoves += 1
            else:
                numberFail += 1
            
            if nOfSmoves == 10000:
                break
        
        #self.run_focusWorseDays()
        print("output", limitRuns - numberFail, numberFail, limitRuns)
       
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
        print("-->",self.startObj, self.penalties.total)
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