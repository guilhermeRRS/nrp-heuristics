# coding=utf-8
from gurobipy import GRB
import logging
import random

def start(self, I, D, T, m, x):
	
	solution = self.solution
	
	objVal = -1

	for i in range(I):
		for d in range(D):
			for t in range(T):
				x[i][d][t].ub = solution[i][d][t]
				x[i][d][t].lb = solution[i][d][t]
	
	m.optimize()
	if m.Status != GRB.OPTIMAL:
		logging.warning("FAILED START "+str(m.Status)+" "+str(m.SolCount))
		return False, objVal
	
	objVal = m.objVal
				
	return True, objVal
	
def unfixVars(self, solution, x, Is, Ds):
	for i in Is:
		for d in Ds:
			for t in range(len(self.sets.T)):
				x[i][d][t].Start = solution[i][d][t]
				x[i][d][t].lb = 0
				x[i][d][t].ub = 1
				
def fixVars(self, solution, x, Is, Ds):
	for i in Is:
		for d in Ds:
			for t in range(len(self.sets.T)):
				value = 1 if x[i][d][t].x >= 0.5 else 0
				x[i][d][t].lb = value
				x[i][d][t].ub = value
				solution[i][d][t] = value
	return solution
				
def fixVarsSol(self, solution, x, Is, Dc, Ds):
	for i in Is:
		for d in range(Dc, Dc + Ds):
			for t in range(len(self.sets.T)):
				value = 1 if solution[i][d][t] >= 0.5 else 0
				x[i][d][t].lb = value
				x[i][d][t].ub = value
	return solution
	
def getDirection(self, nurse, day, shift):
	direcao = 0
	D = self.D
	if shift >= 0:
		tipo = 1
		if day == 0:
			if self.getShift(self.v_x[nurse][day+1]) < 0:
				direcao = 1
		elif day == D-1:
			if self.getShift(self.v_x[nurse][day-1]) < 0:
				direcao = -1
		else:
			if random.randint(0,1):
				if self.getShift(self.v_x[nurse][day+1]) < 0:
					direcao = 1
				else:
					if self.getShift(self.v_x[nurse][day-1]) < 0:
						direcao = -1
			else:
				if self.getShift(self.v_x[nurse][day-1]) < 0:
					direcao = -1
				else:
					if self.getShift(self.v_x[nurse][day+1]) < 0:
						direcao = 1
	else:
		tipo = 0
		if day == 0:
			if self.getShift(self.v_x[nurse][day+1]) >= 0:
				direcao = 1
		elif day == D-1:
			if self.getShift(self.v_x[nurse][day-1]) >= 0:
				direcao = -1
		else:
			if random.randint(0,1):
				if self.getShift(self.v_x[nurse][day+1]) >= 0:
					direcao = 1
				else:
					if self.getShift(self.v_x[nurse][day-1]) >= 0:
						direcao = -1
			else:
				if self.getShift(self.v_x[nurse][day-1]) >= 0:
					direcao = -1
				else:
					if self.getShift(self.v_x[nurse][day+1]) >= 0:
						direcao = 1
	return tipo, direcao

def get_extremeShifts(self, l_t):

	shortestShiftSize = l_t[0]
	longestShiftSize = l_t[0]
	for i in l_t:
		if i < shortestShiftSize:
			shortestShift = i
		if i > longestShiftSize:
			longestShiftSize = i
	return shortestShiftSize, longestShiftSize