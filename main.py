# coding=utf-8
from model import NurseModel
from solver import Solver
from chronos import Chronos

PATH_DATA = "../instancias/"
PATH_MODEL = "../modelos/"
PATH_SOLUTION = "../initial/"

instance = "10"

chronos = Chronos("aaaaa.log", 1)

chronos.startCounter("Teste")

print(chronos.timeMarks[-1])

chronos.timeMarks[-1].stop = 5

print(chronos.timeMarks[-1])

input()

print(chronos.timeMarks[-1])

chronos.startCounter("Iterando")

chronos.stopCounter()

chronos.stopCounter()

'''
nurse = NurseModel()
nurse.setPathData(f"{PATH_DATA}Instance{instance}.txt")
nurse.setPathModel(f"{PATH_MODEL}modelo{instance}.lp")
nurse.setPathSolution(f"{PATH_SOLUTION}{instance}.sol")

nurse.getData()
nurse.getModel()
nurse.getSolution()

print(nurse)
input()
solver = Solver(nurse)
nurse = solver.run(5)
print(nurse)

print(nurse.solution.printSolution(instance, nurse.data.sets))
'''