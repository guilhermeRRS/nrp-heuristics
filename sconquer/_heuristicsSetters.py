# coding=utf-8
import gurobipy as gp
from gurobipy import GRB

def setDays(self, m, dm_x, minimumNumberOfDays, maximumNumberOfDays, horizonSize, fixedSchedule = []):

	numberOfDays = 0
	
	if len(fixedSchedule) == 0:
		numberOfDaysConstraint_min = m.addConstr(minimumNumberOfDays <= gp.quicksum(dm_x[j] for j in range(horizonSize)))
		numberOfDaysConstraint_max = m.addConstr(gp.quicksum(dm_x[j] for j in range(horizonSize)) <= maximumNumberOfDays)
	else:
		for i in range(horizonSize):
			dm_x[i].lb = fixedSchedule[i]
			dm_x[i].ub = fixedSchedule[i]
	m.update()
	m.optimize()
	if len(fixedSchedule) == 0:
		m.remove(numberOfDaysConstraint_min)
		m.remove(numberOfDaysConstraint_max)
	
	if m.SolCount == 0:
		return -1
	
	for j in range(horizonSize):
		if(dm_x[j].x >= 0.5):
			numberOfDays += 1
			
	return numberOfDays
	
def setShifts(self, m, sm_x, dm_x, horizonSize, sizeT, l_t):

	numberOfHours = 0
	
	daysConstraint = []
	for j in range(horizonSize):
		daysConstraint.append(m.addConstr(gp.quicksum(sm_x[j][k] for k in range(sizeT)) <= (1 if dm_x[j].x >= 0.5 else 0)))
	m.update()
	m.optimize()
	
	for j in range(horizonSize):
		m.remove(daysConstraint[j])
	
	if m.SolCount == 0:
		return -1
	
	for j in range(horizonSize):
		for k in range(sizeT):
			if(sm_x[j][k].x >= 0.5):
				numberOfHours += l_t[k]
			
	return numberOfHours