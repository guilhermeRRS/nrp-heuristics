class Model() :

    pathData = None
    pathModel = None
    pathSolution = None

    data = None
    model = None
    solution = None

    from ._setters import setPathData, setPathModel, setPathSolution, unsetPathData, unsetPathModel, unsetPathSolution

    from ._collectData import _get_data
    from ._collectModel import _get_model
    from ._collectSolution import _get_solution
    from ._writeModel import _write_model

    def getData(self):
        if self.pathData != None:
            self.data = self._get_data()
            if self.data[0]:
                self.I = len(self.data[1]["I"])
                self.D = len(self.data[1]["D"])
                self.T = len(self.data[1]["T"])
                self.W = len(self.data[1]["W"])
            else:
                self.data = None
        else:
            self.data = None

    def getModel(self):
        if self.pathModel != None:
            if self.data != None:
                self.model = self._get_model(self.pathModel, self.I, self.D, self.T, self.W)
            else:
                self.model = None
        else:
            self.model = None

    def getSolution(self):
        if self.pathSolution != None:
            self.solution = self._get_solution()
        else:
            self.solution = None