# coding=utf-8

FAILED_TO_SOLVE = "FAILED_TO_SOLVE"

import gurobipy as gp
from gurobipy import GRB

import logging
import sys
from model import NurseModel
from solver import Solver
from chronos import Chronos

cluster = len((sys.argv[1:])) == 4

PATH_DATA = "instances/dados/" if cluster else "../instancias/"
PATH_MODEL = "instances/modelos/" if cluster else "../modelos/"
PATH_SAVE_SOLUTION = "o_solutions/"
PAT_LOG = "o_logs/"

instance = str(int((sys.argv[1:])[0]))
timeLimit = int((sys.argv[1:])[1])
description = str(((sys.argv[1:])[2]))
fast = True if str(((sys.argv[1:])[3])) == "1" else False

logging.basicConfig(level=logging.DEBUG, filename=f'{PAT_LOG}{instance}_{description}.log', filemode='w', format='%(message)s')
logging.getLogger("gurobipy.gurobipy").disabled = True

nurse = NurseModel()
nurse.setPathData(f"{PATH_DATA}Instance{instance}.txt")
nurse.setPathModel(f"{PATH_MODEL}modelo{instance}.lp")

nurse.getData()
nurse.getModel()

chronos = Chronos(timeLimit = timeLimit)

if nurse.s_data and nurse.s_model:
    
    solver = Solver(nurseModel = nurse, chronos = chronos)
    success, nurse = solver.run(fast = fast)

    print(success)
    if success:
        print(nurse.solution.printSolution(f"{PATH_SAVE_SOLUTION}{instance}_{description}.sol", nurse.data.sets))
    else:
        chronos.printMessage(FAILED_TO_SOLVE)
    
    print(chronos.done())