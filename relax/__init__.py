# coding=utf-8
from chronos import Chronos
from interface import MipInterface
from model import GurobiOptimizedOutput, NurseModel, Solution
from partition import Partition, PartitionHolder, PartitionSize
import gurobipy as gp
from gurobipy import GRB

ORIGIN_RELAX = "ORIGIN_RELAX"

START_ITERATION = "START_ITERATION"
SOLVER_GUROBI_OUTPUT = "SOLVER_GUROBI_OUTPUT"
SOLVER_ITERATION_NO_SOLUTION = "SOLVER_ITERATION_NO_SOLUTION"
SOLVER_ITERATION_NO_TIME = "SOLVER_ITERATION_NO_TIME"

class Relax(MipInterface):

    partitionHolder: PartitionHolder
    chronos: Chronos

    def __init__(self, nurseModel: NurseModel, chronos: Chronos, iPartitionSize: PartitionSize, dPartitionSize: PartitionSize, tPartitionSize:PartitionSize = None, pathPartialSols: str = None):
        super().__init__(nurseModel.model)

        self.nurseModel = nurseModel
        self.chronos = chronos
        
        self.partitionHolder = PartitionHolder(nurseModel.I, nurseModel.D, nurseModel.T)
        self.partitionHolder.createPartition(iPartitionSize, dPartitionSize, tPartitionSize)

        self.pathPartialSols = pathPartialSols

    def run(self, fast:bool = False, factibilize:bool = False):
        
        success = True

        iteration = 0

        donePartitions = []
        partitionsRollback = 0

        m = self.nurseModel.model.m
        
        if fast:
            m.setParam("Solutionlimit", 1)
        
        self.relaxWindow(partition = self.partitionHolder.all())
        while self.partitionHolder.partitionSize() > 0 and success:
            iteration += 1
            success = False
            currentPartition = self.partitionHolder.popPartition()
            
            self.chronos.printMessage(ORIGIN_RELAX, f"Iteration {iteration}")
            if factibilize:
                if partitionsRollback > 0:
                    self.chronos.printMessage(ORIGIN_RELAX, f"Running rollback number {partitionsRollback}", True)

            self.intWindow(partition = currentPartition)

            if self.chronos.stillValidRestrict():
                m.setParam("TimeLimit", self.chronos.timeLeft()/(self.partitionHolder.partitionSize()+1))
            
                self.chronos.startCounter(START_ITERATION)
                m.optimize()
                self.chronos.stopCounter()

                gurobiReturn = GurobiOptimizedOutput(m)

                self.chronos.printObj(ORIGIN_RELAX, SOLVER_GUROBI_OUTPUT, gurobiReturn)

                Solution().generatePartialX(gurobiReturn.valid(), self.nurseModel.model.x, self.pathPartialSols+f'.{iteration}.partial', self.nurseModel.data.sets)

                if gurobiReturn.valid():

                    if partitionsRollback > 0:
                        self.fixWindows(donePartitions[-1])

                    while(partitionsRollback > 0):
                        self.fixWindows(donePartitions[-1-partitionsRollback])
                        partitionsRollback -= 1

                    self.fixWindows(currentPartition)
                    success = True
                    donePartitions.append(currentPartition)
                
                else:

                    if factibilize and gurobiReturn.status == GRB.INFEASIBLE:
                        self.partitionHolder.partitions.insert(0, currentPartition)
                        self.chronos.printMessage(ORIGIN_RELAX, SOLVER_ITERATION_NO_SOLUTION, False)
                        if len(donePartitions) - partitionsRollback > 0:
                            self.chronos.printMessage(ORIGIN_RELAX, f"Asking rollback number {partitionsRollback+1}", True)
                            self.unfixWindows(donePartitions[-1-partitionsRollback])
                        partitionsRollback += 1
                        success = True
                        
                    else:
                        self.chronos.printMessage(ORIGIN_RELAX, SOLVER_ITERATION_NO_SOLUTION, True)
                
            else:
                self.chronos.printMessage(ORIGIN_RELAX, SOLVER_ITERATION_NO_TIME, False)

        if success and self.partitionHolder.partitionSize() == 0:

            self.nurseModel.solution = Solution().getFromX(self.nurseModel.model.x)
            self.nurseModel.s_solution = True
            return True, self.nurseModel

        return False, self.nurseModel