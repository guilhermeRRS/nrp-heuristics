import random

#if the choosen nurses fails on having at least on alternative sequence each, this function exits
def run_sequenceMany(self, numberOfNurses:int, maxInsideCombinationOf:int = 10000,  worse:bool = False, better:bool = False, equal:bool = False, weight:bool = False):

    allDays = list(range(0, self.nurseModel.D))
    
    if weight:
        day = random.choices(allDays, weights=self.penalties.worstDays)
        day = day[0]
    else:
        day = random.randint(0, self.nurseModel.D-1)

    possibleNurses = []
    for i in range(self.nurseModel.I):
        if day in self.helperVariables.workingDays[i]:
            possibleNurses.append(i)
            
    if len(possibleNurses) == 0:
        return False, None
    
    nurses = random.choices(possibleNurses, k = numberOfNurses)
    nursesOptions = []
    for nurse in nurses:
        s, nurseOptions = self.run_sequence_fixed(nurse, day)
        if s:
            nursesOptions.append(nurseOptions)

    if len(nursesOptions) != numberOfNurses:
        return False, None

    '''
    (preenchimento de pré-processamento) -> para olds (the um append no old, conforme insere-se os intervalos)
    Agora, dentro do rol de combinações possíveis, escolhe-se, avalia-se a função objetivo até max
    '''

    input("--")