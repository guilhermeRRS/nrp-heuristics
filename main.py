# coding=utf-8
from model import NurseModel
from solver import Solver

PATH_DATA = "../instancias/"
PATH_MODEL = "../modelos/"
PATH_SOLUTION = "../initial/"

instance = "10"

nurse = NurseModel()
nurse.setPathData(f"{PATH_DATA}Instance{instance}.txt")
nurse.setPathModel(f"{PATH_MODEL}modelo{instance}.lp")
#nurse.setPathSolution(f"{PATH_SOLUTION}{instance}.sol")
nurse.setPathSolution(f"{instance}.sol")

nurse.getData()
nurse.getModel()
nurse.getSolution()

print(nurse)
input()
solver = Solver(nurse)
nurse = solver.run(5)
print(nurse)

print(nurse.solution.printSolution(instance, nurse.data.sets))