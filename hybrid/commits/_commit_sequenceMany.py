def commit_sequenceMany(self, move):
    newShifts = move["s"]

    #####here, needs to calculate

    for move in newShifts:
        for d in range(move["length"]):
            self.commit_single({"n": move["n"], "d": move["dayStart"]+d, "s": move["s"][d]})