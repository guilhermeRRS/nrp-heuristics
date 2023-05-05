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

    parallelR_t: Dict[int, Dict[int, OneDimInt]]

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

    from .moves._singleInWorkFlow import move_singleInWorkflow, math_singleInWorkflow, apply_singleInWorkflow, const_singleInWorkflow
    from .moves._manyInWorkFlow import math_manyInWorkflow, apply_manyInWorkflow
    from ._utils import generateFromSolution, shiftFreeMark, shiftFreeUnMark

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

    def run_singleInWorkflow(self):
        nurse = random.randint(0, self.nurseModel.I-1)
        day = random.randint(0, self.nurseModel.D-1)
        s, oldShift, newShift = self.move_singleInWorkflow(nurse, day)
        if s:
            pc, dc, tp = self.math_singleInWorkflow(nurse, day, oldShift, newShift)
            #print(pc, dc, tp)
            #print("SINGLE NEW -> ", nurse, day, "|", newShift)
            if self.currentObj > tp:
                print(tp)
                self.currentObj = tp
                self.apply_singleInWorkflow(nurse, day, oldShift, newShift, pc, dc, tp)
                return True
        return False

    def run_manyInWorkflow(self, howMany):
        nurses = []
        day = random.randint(0, self.nurseModel.D-1)
        countTriesNurse = 0

        nursesOldShifts = []
        nursesNewShifts = []

        for i in range(howMany):
            countTriesNurse += 1
            nurse = random.randint(0, self.nurseModel.I-1)
            if nurse not in nurses:
                s, oldShift, newShift = self.move_singleInWorkflow(nurse, day)
                if s:
                    nurses.append(nurse)
                    nursesOldShifts.append(oldShift)
                    nursesNewShifts.append(newShift)

            if countTriesNurse > 100:
                break
              
        if len(nurses) == howMany:
            pc, dc, tp = self.math_manyInWorkflow(nurses, day, nursesOldShifts, nursesNewShifts)
            #print(pc, dc, tp)
            #input()
            #print("SINGLE NEW -> ", nurse, day, "|", newShift)
            if self.currentObj > tp:
                print(tp)
                self.currentObj = tp
                self.apply_manyInWorkflow(nurses, day, nursesOldShifts, nursesNewShifts, pc, dc, tp)
                return True
        return False

    

    def runNeighbourhoods(self):
        singleInWorkflow = 0
        while self.chronos.stillValidRestrict() and singleInWorkflow < 1000:
            if self.run_singleInWorkflow():
                singleInWorkflow = 0
            else:
                singleInWorkflow += 1
        
        for howMany in range(2, 9):
            print("!!!!!!!!!!!!!!!!!!!")
            manyInWorkflow = 0
            while self.chronos.stillValidRestrict() and manyInWorkflow < howMany*10000:
                if self.run_manyInWorkflow(howMany):
                    manyInWorkflow = 0
                else:
                    manyInWorkflow += 1


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
            self.chronos.printMessage(ORIGIN_SOLVER, SOLVER_ITERATION_NO_SOLUTION, False)
            
        self.chronos.printMessage(ORIGIN_SOLVER, "NOT_ABLE_TO_SAVE", True)
            
        return False, self.nurseModel