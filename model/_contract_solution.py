# coding=utf-8
import gurobipy as gp
from gurobipy import GRB
from typing import List, NewType
import io
from ._contract_data import Sets

MEMBER_OF_SOLUTION = "MEMBER_OF_SOLUTION"

ThreeDimInt = NewType("ThreeDimInt", List[List[List[int]]]);
ThreeDimVar = NewType("threeDimVar", List[List[List[gp.Var]]]);

class Solution:
    solution: ThreeDimInt

    def loadSolution(self, solution: ThreeDimInt):
        self.solution = solution
        return self

    def printSolution(self, path: str, sets: Sets):
	
        if self.solution:
	    
            path = path
            x = self.solution
	    
            I = len(sets.I)
            D = len(sets.D)
            T = len(sets.T)

            output = ""
            for i in range(I):
                line = ""
                for d in range(D):
                    shift = ""
                    for t in range(T):
                        if x[i][d][t] >= 0.5:
                            shift = sets.T[t]
                            break
                    line = line+shift+"\t"
                output = output+line+"\n"
				
            solfile = io.open(path, "w+", encoding = "utf8")
            solfile.write(output)

            return True
		
        return False
    
    def getFromX(self, x: ThreeDimVar):
        solution = []
        I = len(x)
        D = len(x[0])
        T = len(x[0][0])
        for i in range(I):
            solution.append([])
            for d in range(D):
                solution[-1].append([])
                for t in range(T):
                    solution[-1][-1].append(0 if x[i][d][t].x < 0.5 else 1)
        
        return self.loadSolution(solution)

    def __str__(self):
        output = f"===== {MEMBER_OF_SOLUTION} =====\nInfos:\n"
        output += f"I:      {len(self.solution)}\n"
        output += f"D:      {len(self.solution[0])}\n"
        output += f"T:      {len(self.solution[0][0])}\n"
        output += f"Hash:   {hash(str(self.solution))}\n"
        output += "==============="
        return output