# coding=utf-8
from model import Model

PATH_DATA = "../instancias/"
PATH_MODEL = "../modelos/"
PATH_SOLUTION = "../initial/"

instance = "10"

nurse = Model()
nurse.setPathData(f"{PATH_DATA}Instance{instance}.txt")
nurse.setPathModel(f"{PATH_MODEL}modelo{instance}.lp")
nurse.setPathSolution(f"{PATH_SOLUTION}{instance}.sol")

nurse.getData()
nurse.getModel()
nurse.getSolution()

print(nurse.solution)