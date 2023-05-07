import random

'''
These functions try to explore a neighbourhood
'''

def run_nurseSingle_daySingle_mustWork(self, anyObj, allowEqual):

    nurse = random.randint(0, self.nurseModel.I-1)
    day = random.choice(self.helperVariables.workingDays[nurse])
    
    change = self.SingleChange(self, nurse, day, anyObj, allowEqual)
    if change.valid:
        input(change.change)
        return True, change

    return False, None