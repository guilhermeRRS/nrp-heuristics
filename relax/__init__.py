from chronos import Chronos
from interface import MipInterface
from model import NurseModel


class Relax(MipInterface):

    def __init__(self, nurseModel: NurseModel, chronos: Chronos):
        super().__init__(nurseModel.model)

    def run(self):
        self.relaxWindow(0, 1, 0, 1, 0, 1)
        print("Well")