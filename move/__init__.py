# coding=utf-8
import gurobipy as gp
from gurobipy import GRB
import os, sys, logging, random, math, time
from decimal import *
import copy

from model import NurseModel

class Move(NurseModel):
	
	from ._helper import start, unfixVars, fixVars, get_extremeShifts
	from ._rules import constraint2, constraint3, constraint3_multi, constraint45, constraint45_multi, constraint678, constraint678_free, constraint678_work, constraint9, constraint9_multi, constraint10, getFreeInterval, getWorkingInterval
	from ._moves import cleanNurseMoveEstimative, setNurseMoveEstimative, validMultiShift
	from ._moves import estimate_demanda_singleNurse, estimate_demanda_manyNurse, validMove_groupNind, estimateMove_groupNind, applyMove_groupNind, estimateMove_groupNSind, validMove_shortInd, estimateMove_shortInd, applyMove_shortInd, estimateMove_shortsInd, applyMove_shortsInd
	from ._selects import selectNeighbourhood_groupNind, selectNeighbourhood_groupNSind, selectNeighbourhood_shortInd, selectNeighbourhood_shortsInd
	from ._selects import getMaiorCmax, simplicaSchedule
	from ._updates import update_x, update_yz, update_k, update_nwl, update_ngs
	from sconquer import Ruin_SConquer

	def herdaSolucao(self, solution, sets, parameters, variables):
		self.I = len(sets.I)
		self.D = len(sets.D)
		self.T = len(sets.T)
		self.W = len(sets.W)
		
		self.solution = solution
		self.reduzaSol()
		self.sets = sets
		self.parameters = parameters
		self.variables = variables
	def reduzaSol(self):
		output = []
		for i in range(self.I):
			output.append([])
			for d in range(self.D):
				output[-1].append(self.getShift(self.solution[i][d]))
		self.solution = output
	def getSetsLen(self, sets):
		#I, D, T, W
		return len(sets.I), len(sets.D), len(sets.T), len(sets.W)

	def getVariables(self, variables):
		#m, x, k, y, z, v
		return variables.m, variables.x, variables.k, variables.y, variables.z, variables.v
	def getShift(self, day):
		for t in range(len(day)):
			if day[t] > 0.5:
				return t
		return -1
	def returnSolution(self):
		return self.expandaSol()
	def expandaSol(self):
		output = []
		for i in range(self.I):
			output.append([])
			for d in range(self.D):
				output[-1].append(self.generateDay(self.solution[i][d]))
		return output

	def generateDay(self, shift):
		day = []
		for i in range(self.T):
			day.append(0)
		if shift >= 0:
			day[shift] = 1
		return day
	
	
	def settaSolution(self, objVal):
		self.objVal = objVal
		
		v_nwl = []
		v_ngs = []
		v_k = []
		for i in range(self.I):
			v_nwl.append(0)
			v_ngs.append([])
			v_k.append([])
			for d in range(self.D):
				if self.solution[i][d] >= 0:
					v_nwl[-1] += self.parameters.l_t[self.solution[i][d]]
			for t in range(self.T):
				v_ngs[-1].append(self.solution[i].count(t))
				
			for w in range(self.W):
				v_k[-1].append(1 if self.solution[i][7*w+5] >= 0 or self.solution[i][7*w+6] >= 0 else 0)
		
		v_x = self.solution
		
		inversa = [list(i) for i in zip(*v_x)]
		
		v_y = []
		v_z = []
		for d in range(self.D):
			v_y.append([])
			v_z.append([])
			for t in range(self.T):
				suprida = inversa[d].count(t)
				if suprida == self.parameters.u[d][t]:
					v_y[-1].append(0)
					v_z[-1].append(0)
				elif suprida > self.parameters.u[d][t]:
					v_y[-1].append(0)
					v_z[-1].append(suprida - self.parameters.u[d][t])
				else:
					v_y[-1].append(self.parameters.u[d][t] - suprida)
					v_z[-1].append(0)
				
		self.v_nwl = v_nwl
		self.v_ngs = v_ngs
		self.v_k = v_k
		self.v_y = v_y
		self.v_z = v_z
	
	def nurseToWord(self, nurse):
		if nurse < 26:
			return chr(nurse+65)
		return "A"+chr((nurse%26)+65)
	
	def nursesToWords(self, nurses):
		output = []
		for nurse in nurses:
			output.append(self.nurseToWord(nurse))
		return output
		
	def dayToday(self,day):
		return day + 6
		
	def daysToday(self, days):
		output = []
		for d in days:
			output.append(self.dayToday(d))
		return output
	
	def criterio_smart(self, bestObj, lastObj, currentObj):
		
		sucesso = True
		
		passo = self.smart_passo
		
		if passo == 0 or passo == 3: #deep
			if currentObj < lastObj:
				self.smart_iter1 = 0
			else:
				self.smart_iter1 += 1
				sucesso = False
				
				if self.smart_iter1 > self.tolerancia[passo]:
					passo += 1
				
		elif passo == 1 or passo == 4: #nostag
			if currentObj < lastObj:
				self.smart_iter1 = 0
				self.smart_iter2 = 0
			elif currentObj == lastObj:
				self.smart_iter1 += 1
				if self.smart_iter1 > self.tolerancia[passo][1]:#se a quantidade de iguais ultrapassa
					sucesso = False
					self.smart_iter2 += 1
					if self.smart_iter2 > self.tolerancia[passo][0]:#se a quantidade de piores ultrapassa
						passo += 1
			else:
				self.smart_iter2 += 1
				sucesso = False
				if self.smart_iter2 > self.tolerancia[passo][0]:#se a quantidade de piores ultrapassa
					passo += 1
		
		elif passo == 2: #worse
			
			self.smart_iter1 += 1
			if self.smart_iter1 > self.tolerancia[passo][0]:
				sucesso = False
				passo += 1
			else:
				if currentObj > lastObj:
					delta = currentObj - lastObj
					if random.random() < math.e**(-delta/self.temperatura):
						sucesso = False
			
			if passo == 2:
				self.temperatura *= self.tolerancia[passo][2]
		
		if passo != self.smart_passo:
			self.smart_iter1 = 0
			self.smart_iter2 = 0
			if passo == 2:
				self.temperatura = self.tolerancia[passo][1]
		
		self.smart_passo = passo
		
		return sucesso, passo > 4
	
	def criterio(self, bobj, obj, newObj):
		saida = False
		if self.criterioMode == "smart":
			saida, escapar = self.criterio_smart(bobj, obj, newObj)
		
		if escapar:
			self.mustLeave = True
		
		return saida
	
	#this function only works for smart approach
	def run(self, last, iters, tempo, sobrou, tolerancia, mode, criterio, criterioParam = False):
		
		self.criterioMode = criterio
		self.tolerancia = tolerancia
		
		if criterio == "smart":
			self.smart_passo = 0
			self.smart_iter1 = 0
			self.smart_iter2 = 0
		
		tempo += sobrou
		
		getcontext().prec = 15
		tempo = Decimal(tempo)
		
		sets, parameters = self.sets, self.parameters
		self.get_extremeShifts(self.parameters.l_t)
		
		I, D, T, W = self.getSetsLen(self.sets)
		self.I = I
		self.D = D
		self.T = T
		self.W = W
		m, x, k, y, z, v = self.getVariables(self.variables)
		
		v_nwl = self.v_nwl
		v_ngs = self.v_ngs
		self.v_x = self.solution
		v_x = self.v_x
		v_k = self.v_k
		v_y = self.v_y
		v_z = self.v_z
		objVal = self.objVal
		sobjVal = objVal
		bobjVal = objVal
		solution = self.solution
		bestSolution = self.solution
		initialSolution = self.solution
		
		print("START", objVal)
		
		#neighbourhoods = ["focused-exchange", "two-exchange", "focused-exchange", "three-exchange", "focused-exchange", "double-exchange", "focused-exchange", "multi-exchange", "focused-exchange", "block-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange", "focused-exchange"]
		'''
		n(s)-sind: nurse(s) single independent - altera um único turno de um nurse(s)
		n(s)-mind: nurse(s) multi independent - altera multiplos turnos não consecutivos de um nurse(s)
		n(s)-bind: nurse(s) block independent - altera um bloco de turnos consecutivos de um nurse(s)
		short-ind: short independent - expande intervalos de folga/trabalho de um nurse
		'''
		#neighbourhoods = ["short-ind", "n-sind", "short-ind", "n-sind", "short-ind", "n-sind", "short-ind", "n-sind", "short-ind", "n-sind", "short-ind", "n-sind", "short-ind", "n-sind", "short-ind", "n-sind", "short-ind", "n-sind", "short-ind", "n-sind", "short-ind", "n-sind", "short-ind", "n-sind", "short-ind", "n-sind", "short-ind", "n-sind", "short-ind", "n-sind", "short-ind", "n-sind", "short-ind", "n-sind", "short-ind", "n-sind", "short-ind", "n-sind", "short-ind", "n-sind", "short-ind", "n-mind", "short-ind", "n-bind", "short-ind", "ns-sind", "short-ind", "ns-mind", "short-ind", "ns-bind", "short-ind", "two-exchange", "short-ind", "three-exchange", "short-ind", "double-exchange", "short-ind", "multi-exchange", "short-ind", "block-exchange", "short-ind"]

		if mode == "random":
			neighbourhoodsOptions = ["n-sind", "n-bind", "n-mind", "ns-sind", "ns-bind", "ns-mind", "short-ind", "shorts-ind"]
			neighbourhoods = []
			for i in range(len(criterioParam)):
				for j in range(criterioParam[i]):
					neighbourhoods.append(neighbourhoodsOptions[i])
		currentNeighbourhood = 0
		bobjVal = sobjVal
		
		initialRunningTime = time.time()
		self.mustLeave = False
		while iters > 0 and tempo > 0 and not self.mustLeave:
			
			if mode == "random":
				currentNeighbourhood = random.randint(0, len(neighbourhoods)-1)
			
			startTime = time.time()
			iters -= 1
			
			if neighbourhoods[currentNeighbourhood%len(neighbourhoods)] in ("n-sind", "n-mind", "n-bind"):
				
				mode = neighbourhoods[currentNeighbourhood%len(neighbourhoods)]
				
				nurse, days, changes = self.selectNeighbourhood_groupNind(tempo, mode)
				
				if nurse < 0:
					break
				#input()
				newObj = self.estimateMove_groupNind(nurse, days, changes, objVal)
				
				if self.criterio(bobjVal, objVal, newObj):
				
					currentNeighbourhood = 0
				
					self.applyMove_groupNind(nurse, days, changes)
					
					if newObj <= bobjVal:
						bobjVal = newObj
						bestSolution = self.v_x
						
					print(iters, mode, self.nurseToWord(nurse), self.daysToday(days), changes, "|", newObj, objVal)
					
					objVal = newObj
				
				else:
					currentNeighbourhood += 1
			
			elif neighbourhoods[currentNeighbourhood%len(neighbourhoods)] in ("ns-sind", "ns-mind", "ns-bind"):
				
				mode = neighbourhoods[currentNeighbourhood%len(neighbourhoods)]
				
				nurses, days, changes = self.selectNeighbourhood_groupNSind(tempo, mode)
				
				if len(nurses) == 0:
					break
				#input()
				
				newObj = objVal
				newObj = self.estimateMove_groupNSind(nurses, days, changes, newObj)
				
				if self.criterio(bobjVal, objVal, newObj):
				
					currentNeighbourhood = 0
				
					for nurse in range(len(nurses)):
						self.applyMove_groupNind(nurses[nurse], days, changes[nurse])
					
					if newObj <= bobjVal:
						bobjVal = newObj
						bestSolution = self.v_x
						
					print(iters, mode, self.nursesToWords(nurses), self.daysToday(days), changes, "|", newObj, objVal)
					
					objVal = newObj
				
				else:
					currentNeighbourhood += 1
			
			elif neighbourhoods[currentNeighbourhood%len(neighbourhoods)] == "short-ind":
					
				nurse, day, changes = self.selectNeighbourhood_shortInd(tempo)
				
				if nurse < 0:
					break
				#input()
				newObj = self.estimateMove_shortInd(nurse, day, changes, objVal)
				
				if self.criterio(bobjVal, objVal, newObj):
				
					currentNeighbourhood = 0
				
					self.applyMove_shortInd(nurse, day, changes)
					
					if newObj <= bobjVal:
						bobjVal = newObj
						bestSolution = self.v_x
						
					print(iters, "short-ind", self.nurseToWord(nurse), self.dayToday(day), self.dayToday(day+len(changes)-1), changes, "|", newObj, objVal)
					
					objVal = newObj
				
				else:
					currentNeighbourhood += 1
			
			elif neighbourhoods[currentNeighbourhood%len(neighbourhoods)] == "shorts-ind":
					
				nurses, days, changes = self.selectNeighbourhood_shortsInd(tempo)
				
				if len(nurses) == 0:
					break
				#input()
				newObj = self.estimateMove_shortsInd(nurses, days, changes, objVal)
				
				if self.criterio(bobjVal, objVal, newObj):
				
					currentNeighbourhood = 0
					print("CHANGES",changes)
					print("NURSES",nurses)
					print("DAYS",days)
					self.applyMove_shortsInd(nurses, days, changes)
					
					if newObj <= bobjVal:
						bobjVal = newObj
						bestSolution = self.v_x
						
					print(iters, "shorts-ind", self.nursesToWords(nurses), "|", newObj, objVal)
					
					objVal = newObj
				
				else:
					currentNeighbourhood += 1
			
			tempo -= Decimal(time.time() - startTime)
		
		print(iters > 0, tempo > 0, self.mustLeave)
		print("Done", sobjVal, "|", objVal, "|", bobjVal)
		
		if last:#must be active if solution gets worse at anytime (in criterio)
			self.solution = self.v_x
			self.objVal = objVal
		else:
			self.solution = bestSolution
			self.objVal = bobjVal
		
		# input()
		return objVal