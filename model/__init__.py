# coding=utf-8
from typing import Union
from ._contract_data import Data
from ._contract_model import Model
from ._contract_solution import Solution
import gurobipy as gp
from gurobipy import GRB

GUROBI_OPTIMIZE_OUTPUT = "GUROBI_OPTIMIZE_OUTPUT"
MEMBER_OF_MODEL = "MEMBER_OF_MODEL"

class GurobiOptimizedOutput:

    status: int
    solCount: int
    
    def __init__(self, status: int, solCount: int):
        self.status = status
        self.solCount = solCount

    def valid(self):
        return not (not (self.status in (GRB.OPTIMAL, GRB.TIME_LIMIT, GRB.SOLUTION_LIMIT)) or self.solCount == 0)
    
    def __str__(self):
        output =  f"===== {GUROBI_OPTIMIZE_OUTPUT} =====\nInfos:\n"
        output += f"Status:      {self.status}\n"
        output += f"SolCount:    {self.solCount}\n"
        output += "==============="
        return output


class NurseModel() :

    pathData: str
    pathModel: str
    pathSolution: str

    data: Data
    s_data: bool
    model: Model
    s_model: bool
    solution: Solution
    s_solution: bool

    def __init__(self):
        self.pathData = None
        self.pathModel = None
        self.pathSolution = None

        self.data = None
        self.s_data = False
        self.model = None
        self.s_model = False
        self.solution = None
        self.s_solution = False

    def __str__(self):
        output =  f"===== {MEMBER_OF_MODEL} =====\nInfos:\n"
        output += f"Is there data:      {self.data != None}\n"
        output += f"Success data:       {self.s_data}\n"
        output += f"Is there model?     {self.model != None}\n"
        output += f"Success model?      {self.s_model}\n"
        output += f"Is there solution?  {self.solution != None}\n"
        output += f"Success solution?   {self.s_solution}\n"
        output += "==============="
        return output

    from ._setters import setPathData, setPathModel, setPathSolution, unsetPathData, unsetPathModel, unsetPathSolution

    from ._collectData import _get_data
    from ._collectModel import _get_model
    from ._collectSolution import _get_solution
    from ._writeModel import _write_model

    def getData(self):
        self.s_data = False
        if self.pathData != None:
            self.s_data, self.data = self._get_data()
            if self.s_data:
                self.I = len(self.data.sets.I)
                self.D = len(self.data.sets.D)
                self.T = len(self.data.sets.T)
                self.W = len(self.data.sets.W)
            else:
                self.data = None
        else:
            self.data = None

    def getModel(self):
        self.s_model = False
        if self.pathModel != None:
            if self.s_data:
                self.s_model, self.model = self._get_model(self.pathModel, self.I, self.D, self.T, self.W)
            else:
                self.model = None
        else:
            self.model = None

    def getSolution(self):
        if self.pathSolution != None:
            self.s_solution, self.solution = self._get_solution(self.pathSolution, self.data)
        else:
            self.solution = None