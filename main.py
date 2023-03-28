# coding=utf-8
import logging
import sys
from model import NurseModel
from solver import Solver
from chronos import Chronos

cluster = True

PATH_DATA = "instances/" if cluster else "../instancias/"
PATH_MODEL = "modelos/" if cluster else "../modelos/"
#PATH_GET_SOLUTION = "initial/" if cluster else "../initial/"
PATH_SAVE_SOLUTION = "o_solutions/"
PAT_LOG = "o_logs/"

instance = str(int((sys.argv[1:])[0]))
timeLimit = int((sys.argv[1:])[1])
description = str(((sys.argv[1:])[2]))

logging.basicConfig(level=logging.DEBUG, filename=f'{PAT_LOG}{instance}_{description}.log', filemode='w', format='%(message)s')
logging.getLogger("gurobipy.gurobipy").disabled = True

nurse = NurseModel()
nurse.setPathData(f"{PATH_DATA}Instance{instance}.txt")
nurse.setPathModel(f"{PATH_MODEL}modelo{instance}.lp")
#nurse.setPathSolution(f"{PATH_GET_SOLUTION}{instance}.sol")

nurse.getData()
nurse.getModel()
#nurse.getSolution()

chronos = Chronos(timeLimit = timeLimit)

if nurse.s_data and nurse.s_model:
    solver = Solver(nurseModel = nurse, chronos = chronos)
    success, nurse = solver.run()

    print(success)
    print(nurse.solution.printSolution(f"{PATH_SAVE_SOLUTION}{instance}_{description}.sol", nurse.data.sets))
    print(chronos.done())