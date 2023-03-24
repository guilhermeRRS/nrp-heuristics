# coding=utf-8
import string
from typing import List, NewType
import io

ThreeDimInt = NewType("ThreeDimInt", List[List[List[int]]]);

class Solution:
    solution: ThreeDimInt

    def __init__(self, solution: ThreeDimInt):
        self.solution = solution

    def printSolution(self, path: string):
	
        if self.solution:
	    
            path = path + ".sol"
            x = self.solution
	    
            I = len(self.solution)
            D = len(self.solution[0])
            T = len(self.solution[0][0])

            output = ""
            for i in range(I):
                line = ""
                for d in range(D):
                    shift = ""
                    for t in range(T):
                        if x[i][d][t] >= 0.5:
                            shift = self.sets["T"][t]
                            break
                    line = line+shift+"\t"
                output = output+line+"\n"
				
            solfile = io.open(path, "w+", encoding = "utf8")
            solfile.write(output)

            return True
		
        return False

    def __str__(self):
        output = "===== Member of Solution =====\nInfos:\n"
        output += f"I:      {len(self.solution)}\n"
        output += f"D:      {len(self.solution[0])}\n"
        output += f"T:      {len(self.solution[0][0])}\n"
        output += f"Hash:   {hash(str(self.solution))}\n"
        output += "==============="
        return output