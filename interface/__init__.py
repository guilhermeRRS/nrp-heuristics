from abc import ABC, abstractmethod
from model import Model
import gurobipy as gp
from gurobipy import GRB

class MipInterface(ABC):

    model:Model

    def __init__(self, model:Model):
        self.model = model

    def relaxWindow(self, i0:int, i9:int, d0:int, d9:int, t0:int, t9:int):
        I = len(self.model.x)
        D = len(self.model.x[0])
        T = len(self.model.x[0][0])
        assert i0 >= 0 and i9 < I
        assert d0 >= 0 and d9 < D
        assert t0 >= 0 and t9 < T
        for d in range(D):
            for i in range(I):
                for t in range(T):
                    
                    self.model.x[i][d][t].vtype = GRB.CONTINUOUS
                    self.model.x[i][d][t].lb = 0
                    self.model.x[i][d][t].ub = 1

                    self.model.v[i][d][t].vtype = GRB.CONTINUOUS
                    self.model.v[i][d][t].lb = 0
                if d % 7 == 6:
                    w = int((d - 6)/7)
                    self.model.k[i][w].vtype = GRB.CONTINUOUS
                    self.model.k[i][w].lb = 0
                    self.model.k[i][w].ub = 1
            for t in range(T):
                self.model.y[d][t].vtype = GRB.CONTINUOUS
                self.model.y[d][t].lb = 0
                self.model.z[d][t].vtype = GRB.CONTINUOUS
                self.model.z[d][t].lb = 0

    def intWindow(self, i0:int, i9:int, d0:int, d9:int, t0:int, t9:int):
        I = len(self.model.x)
        D = len(self.model.x[0])
        T = len(self.model.x[0][0])
        assert i0 >= 0 and i9 < I
        assert d0 >= 0 and d9 < D
        assert t0 >= 0 and t9 < T

        for d in range(D):
            for i in range(I):
                for t in range(T):
                    
                    self.model.x[i][d][t].vtype = GRB.BINARY

                    self.model.v[i][d][t].vtype = GRB.INTEGER
                if d % 7 == 6:
                    w = int((d - 6)/7)
                    self.model.k[i][w].vtype = GRB.BINARY
            for t in range(T):
                self.model.y[d][t].vtype = GRB.INTEGER
                self.model.z[d][t].vtype = GRB.INTEGER

    def fixWindows(self, i0:int, i9:int, d0:int, d9:int, t0:int, t9:int):
        I = len(self.model.x)
        D = len(self.model.x[0])
        T = len(self.model.x[0][0])
        assert i0 >= 0 and i9 < I
        assert d0 >= 0 and d9 < D
        assert t0 >= 0 and t9 < T

        for i in range(I):
            for d in range(D):
                for t in range(T):
                    newVal = 1 if self.model.x[i][d][t].x >= 0.5 else 0
                    self.model.x[i][d][t].lb = newVal
                    self.model.x[i][d][t].ub = newVal

    def unfixWindows(self, i0:int, i9:int, d0:int, d9:int, t0:int, t9:int):
        I = len(self.model.x)
        D = len(self.model.x[0])
        T = len(self.model.x[0][0])
        assert i0 >= 0 and i9 < I
        assert d0 >= 0 and d9 < D
        assert t0 >= 0 and t9 < T

        for i in range(I):
            for d in range(D):
                for t in range(T):
                    self.model.x[i][d][t].lb = 0
                    self.model.x[i][d][t].ub = 1