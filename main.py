# coding=utf-8
import logging
from model import NurseModel
from solver import Solver
from chronos import Chronos

PATH_DATA = "../instancias/"
PATH_MODEL = "../modelos/"
PATH_SOLUTION = "../initial/"

instance = "10"

logging.basicConfig(level=logging.DEBUG, filename=f'{instance}.log', filemode='w', format='%(message)s')
logging.getLogger("gurobipy.gurobipy").disabled = True

nurse = NurseModel()
nurse.setPathData(f"{PATH_DATA}Instance{instance}.txt")
nurse.setPathModel(f"{PATH_MODEL}modelo{instance}.lp")
nurse.setPathSolution(f"{PATH_SOLUTION}{instance}.sol")

nurse.getData()
nurse.getModel()
#nurse.getSolution()

chronos = Chronos(5)

solver = Solver(nurseModel = nurse, chronos = chronos)
success, nurse = solver.run()

print(success)
print(nurse.solution.printSolution(f"{instance}.sol", nurse.data.sets))
print(chronos.done())