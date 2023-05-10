# coding=utf-8
import json
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

    from ._utils import preProcessFromSolution, getPreProcessData, preProcess, computeLt, generateShiftPre, shiftFreeMark, shiftFreeUnMark, getOptions, evaluateFO

    from .rules._forSingle import const_single, math_single, math_single_demand, math_single_preference, math_single_demandDelta, math_single_preferenceDelta
    from .rules._forSequence import min_max_possible_workload, const_sequence, math_sequence, math_manyNurses_daySequence, math_demandSingleShift_manyNurses_daySequence
    
    from .runs._run_single import run_single, const2_verify
    from .runs._run_sequence import run_sequence, getSequenceWorkMarks, getOptions, run_sequence_fixed
    from .runs._run_sequenceMany import run_sequenceMany
    #from .runs._run_focusWorseDays import run_focusWorseDays
    
    from .commits._commit_single import commit_single
    from .commits._commit_sequence import commit_sequence
    from .commits._commit_sequenceMany import commit_sequenceMany

    
    def __init__(self, nurseModel: NurseModel, instance, chronos: Chronos):
        self.nurseModel = nurseModel
        self.instance = instance
        self.chronos = chronos
        self.helperVariables = HelperVariables()
        self.penalties = penalties()

    def runNeighbourhoods(self):
        
        print("Mais rápido")
        #first we do the quickest movement -> this helps a faster exploration of space in larger instances 
        while self.chronos.stillValidRestrict():
            numberSuccess = 0
            for i in range(10000):
                s, move = self.run_single(worse = False, better = True, equal = False)
                if s:
                    self.commit_single(move)
                    numberSuccess += 1
                if not self.chronos.stillValidRestrict():
                    break

            print(numberSuccess)
            if numberSuccess < 10:
                break

        print("~~~~~>",self.penalties.total)
        print("Segunda mais rápida")
        #then we run the second fastest move
        maxIters = self.highest_cmax
        while self.chronos.stillValidRestrict():
            numberSuccess = 0
            for i in range(1000):
                s, move = self.run_sequence(sizeSampleOptions = maxIters, worse = False, better = True, equal = False)
                if s:
                    self.commit_sequence(move)
                    numberSuccess += 1
                    
                if not self.chronos.stillValidRestrict():
                    break
            
            print(numberSuccess)
            if numberSuccess < 10:
                break
        print("~~~~~>",self.penalties.total)
        print("Mais custosa")
        #finally run the most expesive move
        for numberOfNurses in [2, 3, 5, 8, 10, 12, 15]:
        #for numberOfNurses in [2]:
            print("--->", numberOfNurses)
            maxIters = numberOfNurses*self.highest_cmax
            while self.chronos.stillValidRestrict():
                numberSuccess = 0
                for i in range(1000):
                    s, move = self.run_sequenceMany(numberOfNurses = numberOfNurses, maxInsideCombinationOf = maxIters, maxSampled = int(maxIters/numberOfNurses), worse = False, better = True, equal = False)
                    if s:
                        self.commit_sequenceMany(move)
                        numberSuccess += 1
                        
                    if not self.chronos.stillValidRestrict():
                        break
                    
                print(numberSuccess)
                if numberSuccess < 10:
                    break
            if not self.chronos.stillValidRestrict():
                break
        
        #self.run_focusWorseDays()
    
    def runNeighbourhoods_teste(self):

        s, move = self.run_nurseSequenceRewrite(rangeOfSequences = 1, worse = False, better = True, equal = False)
        
        
        #self.run_focusWorseDays()
    

    def run(self, startObj):
        m = self.nurseModel.model.m
        self.startObj = startObj
        self.currentObj = startObj
        self.chronos.startCounter("SETTING_START")
        self.getPreProcessData()
        self.chronos.stopCounter()
        print("Start working")
        while self.chronos.stillValidRestrict():

            self.runNeighbourhoods_teste()
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