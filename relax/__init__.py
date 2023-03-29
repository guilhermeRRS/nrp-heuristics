from chronos import Chronos
from interface import MipInterface
from model import GurobiOptimizedOutput, NurseModel, Solution
from partition import Partition, PartitionHolder, PartitionSize

RELAX = "RELAX"

START_ITERATION = "START_ITERATION"
SOLVER_GUROBI_OUTPUT = "SOLVER_GUROBI_OUTPUT"
SOLVER_ITERATION_NO_SOLUTION = "SOLVER_ITERATION_NO_SOLUTION"
SOLVER_ITERATION_NO_TIME = "SOLVER_ITERATION_NO_TIME"

class Relax(MipInterface):

    partitionHolder: PartitionHolder
    chronos: Chronos

    def __init__(self, nurseModel: NurseModel, chronos: Chronos, iPartitionSize: PartitionSize, dPartitionSize: PartitionSize, tPartitionSize:PartitionSize = None):
        super().__init__(nurseModel.model)

        self.chronos = chronos
        self.chronos.origin = RELAX
        
        self.partitionHolder = PartitionHolder(nurseModel.I, nurseModel.D, nurseModel.T)
        self.partitionHolder.createPartition(iPartitionSize, dPartitionSize, tPartitionSize)

    def run(self, fast:bool = False):
        
        success = True

        m = self.nurseModel.model.m
        
        if fast:
            m.setParam("Solutionlimit", 1)
        
        self.relaxWindow(partition = self.partitionHolder.all())
        while self.partitionHolder.partitionSize() > 0:
            success = False
            self.intWindow(partition = self.partitionHolder.popPartition())

            if self.chronos.stillValidRestrict():
                m.setParam("TimeLimit", self.chronos.timeLeft())
            
                self.chronos.startCounter(START_ITERATION)
                m.optimize()
                self.chronos.stopCounter()

                gurobiReturn = GurobiOptimizedOutput(m.Status, m.SolCount)

                self.chronos.printObj(SOLVER_GUROBI_OUTPUT, gurobiReturn)

                if gurobiReturn.valid():

                    success = True
                
                else:
                    self.chronos.printMessage(SOLVER_ITERATION_NO_SOLUTION, False)
                
            else:
                self.chronos.printMessage(SOLVER_ITERATION_NO_TIME, False)

        if success and self.partitionHolder.partitionSize() == 0:

            self.nurseModel.solution = Solution().getFromX(self.nurseModel.model.x)
            self.nurseModel.s_solution = True
            return True, self.nurseModel

        return False, self.nurseModel