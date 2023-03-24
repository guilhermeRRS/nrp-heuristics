# coding=utf-8
from typing import List, NewType
import gurobipy as gp
from gurobipy import GRB

twoDimVar = NewType("twoDimVar", List[List[gp.Var]]);
threeDimVar = NewType("threeDimVar", List[List[List[gp.Var]]]);

class Model:
    m: gp.Model;
    x: threeDimVar;
    k: twoDimVar;
    y: twoDimVar;
    z: twoDimVar;
    v: threeDimVar;

    def __init__(self, m: gp.Model, x: threeDimVar, k: twoDimVar, y: twoDimVar, z: twoDimVar, v: threeDimVar):
        self.m = m
        self.x = x
        self.k = k
        self.y = y
        self.z = z
        self.v = v

    def __str__(self):
        output = "===== Member of Model =====\nInfos:\n"
        output += f"I: {len(self.x)}\n"
        output += f"D: {len(self.x[0])}\n"
        output += f"T: {len(self.x[0][0])}\n"
        output += "==============="
        return output