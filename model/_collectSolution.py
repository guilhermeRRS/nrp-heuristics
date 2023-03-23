# coding=utf-8
import io, logging

'''
This function is responsable for collecting a solution, saved in a file as if it would be tested in RosterViewer

ANY BROKEN SOLTUION (NOT FOLLOWING THE 'STANDARDS') WILL CAUSE UNEXPECTED BEHAVIOR

'''

def readFile(path):
    sucess = True
    fileConteds = []

    try:	
        with io.open(path, "r", encoding = "utf8") as file:		
            fileConteds = file.read()
    except:
        sucess = False
        logging.exception("File not found "+path)
        
    return sucess, fileConteds
    
def _get_solution(self, path, sets):

    solution = []
    
    sucess, fileConteds	= readFile(path)
    if(sucess):
    
        I = len(sets["I"])
        D = len(sets["D"])
        T = len(sets["T"])

        fileConteds = fileConteds.split("\n")
        
        if len(fileConteds) < I:
            sucess = False
        
        if sucess:
        
            for i in range(I):
                solution.append([])
                line = fileConteds[i].split("\t")
                for d in range(D):
                    solution[-1].append([])
                    for t in range(T):
                        solution[-1][-1].append(0)
                    if line[d] != "":
                        solution[-1][-1][sets["T"].index(line[d])] = 1
        
    return sucess, solution