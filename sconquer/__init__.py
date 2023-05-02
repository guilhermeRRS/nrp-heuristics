# coding=utf-8
import math, io, logging, random
from decimal import *
import gurobipy as gp
from gurobipy import GRB

class Ruin_SConquer():

	from ._collectData import readFile, splitFile, work_horizon, work_shift, work_staff, work_daysOff, work_shiftOn_or_OffRequests, work_cover, get_data, convertFormat
	from ._createModels import create_days_model, create_shift_model
	from ._heuristicsSetters import setDays, setShifts 

	def get_extremeShifts(self, l_t):

		shortestShiftSize = l_t[0]
		longestShiftSize = l_t[0]
		for i in l_t:
			if i < shortestShiftSize:
				shortestShift = i
			if i > longestShiftSize:
				longestShiftSize = i
		return shortestShiftSize, longestShiftSize
	
	def getPattern(self, solution):
		pattern = []
		for d in range(self.D):
			pattern.append(1 if solution[d].x >= 0.5 else 0)
		return pattern
	
	#foco True: procurar novas estruturas, caso contrário, preencher com turnos as já conhecidas
	def run(self, sets, parameters, nurse, itersLimit, time, schedulesConhecidos, foco):
		newKnownStructures = []
		
		exceededTime = False
		
		getcontext().prec = 10
		time = Decimal(time)
		
		shortestShiftSize, longestShiftSize = self.get_extremeShifts(parameters["l_t"])

		all_days = []

		horizonSize = len(sets["D"])
		self.D = horizonSize
		sizeT = len(sets["T"])

		i = nurse
		
		days_model, dm_x, dm_k = self.create_days_model(i, sets, parameters)
		#aqui vamos impedir que seja fornecida uma mesma estrutura de solução já inserida no banco previamente
		if foco:
			for schedule in schedulesConhecidos:
				scheduleAtual = schedule
				workDays = [i for i, x in enumerate(scheduleAtual) if x >= 0.5]
				freeDays = [i for i, x in enumerate(scheduleAtual) if x < 0.5]
				days_model.addConstr(gp.quicksum((1 - dm_x[i]) for i in workDays) + gp.quicksum((dm_x[i]) for i in freeDays) >= 1)
		
		days_model.setParam("OutputFlag",0)
		days_model.setParam('Solutionlimit', 1)
		
		shift_model, sm_x = self.create_shift_model(i, sets, parameters)
		shift_model.setParam("OutputFlag",0)
		shift_model.setParam('Solutionlimit', 1)
		
		minimumNumberOfDays = math.ceil(parameters["b_min"][i]/longestShiftSize)
		maximumNumberOfDays = math.floor(parameters["b_max"][i]/shortestShiftSize)
		
		tighten = True #True if should increase minimum, False if Maximum
		iters = 0
		success = False
		first = True
		while iters < itersLimit:
			
			if(time <= 0):
				exceededTime = True
				break
		
			days_model.setParam("Timelimit", time)
			if foco:
				numberOfDays = self.setDays(days_model, dm_x, minimumNumberOfDays, maximumNumberOfDays, horizonSize)
			else:
				numberOfDays = self.setDays(days_model, dm_x, minimumNumberOfDays, maximumNumberOfDays, horizonSize, random.choice(schedulesConhecidos))
			timeTaken = Decimal(days_model.Runtime)
			time -= timeTaken
			if(time <= 0):
				exceededTime = True
				break
			
			if numberOfDays > -1:
				newKnownStructures.append(self.getPattern(dm_x))
				first = False
				days_model.setParam("Timelimit", time)
				numberOfHours = self.setShifts(shift_model, sm_x, dm_x, horizonSize, sizeT, parameters["l_t"])
				timeTaken = Decimal(days_model.Runtime)
				time -= timeTaken
				
				if numberOfHours > -1:
					success = True
					break
				
				if tighten:
					minimumNumberOfDays += 1
				else:
					maximumNumberOfDays -= 1
			
			else: #sure we wont get here at the first interation otherwise the problem is infeasible (what we assume to be false)
				
				if first:
					break
				
				if tighten:
					maximumNumberOfDays += 1
					maximumNumberOfDays = min(horizonSize, maximumNumberOfDays)
				else:
					minimumNumberOfDays -= 1
					maximumNumberOfDays = max(0, minimumNumberOfDays)
					
				tighten = not tighten
				
			iters += 1
			
		solution = []
		if success:
			for d in range(horizonSize):
				solution.append(-1)
				for t in range(sizeT):
					if sm_x[d][t].x >= 0.5:
						solution[d] = t
		
		if foco:
			addedKnownStructures = []
			for structure in newKnownStructures:
				if addedKnownStructures.count(structure) == 0:
					addedKnownStructures.append(structure)
					schedulesConhecidos.append(structure)
		return solution, schedulesConhecidos