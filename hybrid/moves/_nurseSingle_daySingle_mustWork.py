def move_nurseSingle_daySingle_mustWork(self, nurse, day):

    if self.helperVariables.workingDays[nurse].count(day) < 0:
        return False, -1
    
    currentDay = self.helperVariables.workingDays[nurse][day]

    allOptions = self.getOptions(self, nurse, day, day, 1)

    for i in range(len(allOptions)):
        if not self.verifyWorkload(nurse, self.nurseModel.data.parameters.l_t[currentDay], allOptions[i]):
            return False, -1
        if not self.verifyMaxShifts(self, nurse, [currentDay], allOptions[i]):
            return False, -1
        
    return True    
    
#def commit_nurseSingle_daySingle_mustWork