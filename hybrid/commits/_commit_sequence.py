def commit_sequence(self, move):
    nurse = move["n"]
    day = move["d"]
    newShifts = move["s"]

    for i in range(len(newShifts)):
        self.commit_single({"n": nurse, "d": day+i, "s": newShifts[i]})