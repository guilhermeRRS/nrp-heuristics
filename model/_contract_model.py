# coding=utf-8
from typing import List, NewType
import gurobipy as gp
from gurobipy import GRB

twoDimVar = NewType("twoDimVar", List[List[gp.Var]]);
threeDimVar = NewType("threeDimVar", List[List[List[gp.Var]]]);

class Model:
    x: threeDimVar;
    k: twoDimVar;
    y: twoDimVar;
    z: twoDimVar;
    v: threeDimVar;

    def __init__(self, x: threeDimVar, k: twoDimVar, y: twoDimVar, z: twoDimVar, v: threeDimVar):
        self.x = x
        self.k = k
        self.y = y
        self.z = z
        self.v = v