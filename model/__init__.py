# coding=utf-8
import string
from typing import Union
from ._contract_data import Data
from ._contract_model import Model
from ._contract_solution import Solution

class Model() :

    pathData: string
    pathModel: string
    pathSolution: string

    data: Data
    s_data: bool
    model: Model
    s_model: bool
    solution: Solution

    from ._setters import setPathData, setPathModel, setPathSolution, unsetPathData, unsetPathModel, unsetPathSolution

    from ._collectData import _get_data
    from ._collectModel import _get_model
    from ._collectSolution import _get_solution
    from ._writeModel import _write_model

    def getData(self):
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
        if self.pathModel != None:
            if self.data != None:
                self.model = self._get_model(self.pathModel, self.I, self.D, self.T, self.W)
            else:
                self.model = None
        else:
            self.model = None

    def getSolution(self):
        if self.pathSolution != None:
            self.solution = self._get_solution()
        else:
            self.solution = None