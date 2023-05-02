# coding=utf-8
import gurobipy as gp
from gurobipy import GRB
import os, sys, logging, random, math, time
from decimal import *
import copy

from model import NurseModel
from move import Move

class Hybrid(NurseModel):
	
	from ._helper import start, unfixVars, fixVars, fixVarsSol, getDirection
	def getSetsLen(self, sets):
		#I, D, T, W
		return len(sets.I), len(sets.D), len(sets.T), len(sets.W)

	def __init__(self, nurseModel: NurseModel):
		self.sets = nurseModel.data.sets
		self.parameters = nurseModel.data.parameters
		self.model = nurseModel.model
		self.solution = nurseModel.solution.solution
	
	def pesaSol(self, solution, numeroPiores, rangePiores, cotaDias, cotaNurse):
	
		I, D, T, W = self.getSetsLen(self.sets)
		cotaDias = min(D, math.ceil(cotaDias))
		
		demandaSaciada = []
		pesosDias = []
		for d in range(D):
			demandaSaciada.append([])
			for t in range(T):
				nursesWorking = sum(solution[i][d][t] for i in range(I))
				if nursesWorking < self.parameters.u[d][t]:
					demandaSaciada[-1].append((self.parameters.u[d][t] - nursesWorking)*self.parameters.w_min[d][t]/(I*T))
				elif nursesWorking > self.parameters.u[d][t]:
					demandaSaciada[-1].append((self.parameters.u[d][t] - nursesWorking)*self.parameters.w_max[d][t]/(I*T))
			pesosDias.append(sum(demandaSaciada[-1]))
			
		numeroDiasAceitar = min(numeroPiores, D)
		
		linhasDias = sorted(range(D), key=lambda x: pesosDias[x])[-numeroDiasAceitar:]
		
		for i in range(numeroDiasAceitar):
			for d in range(linhasDias[i] - math.ceil(rangePiores), linhasDias[i] + math.ceil(rangePiores) + 1):			
				if d>=0 and d<D:
					linhasDias.append(d)
		
		linhasDias = list(dict.fromkeys(linhasDias))
		
		while len(linhasDias) < cotaDias and len(linhasDias) < D:
			newDias = random.randint(0, D-1)
			if linhasDias.count(newDias) == 0:
				linhasDias.append(newDias)
				
				allowedRange = math.floor(random.triangular(1, min(7, cotaDias - len(linhasDias)), 2))
				if allowedRange > 0:
					for d in range(newDias, min(D-1, newDias + allowedRange)):
						linhasDias.append(d)
				
				linhasDias = list(dict.fromkeys(linhasDias))
		
		if cotaNurse != I:
			
			pesosNurses = []
			for i in range(I):
				pesosNurses.append(0)
				for d in range(D):
					for t in range(T):
						if solution[i][d][t]:
							pesosNurses[-1] += self.parameters.p[i][d][t]
						else:
							pesosNurses[-1] += self.parameters.q[i][d][t]
			
			worseNurses = random.randint(0, math.floor(cotaNurse*0.5))
			if worseNurses > 0:
				linhasNurse = sorted(range(I), key=lambda x: pesosNurses[x])[-worseNurses:]
			else:
				linhasNurse = []
			while len(linhasNurse) < cotaNurse:
				newNurse = random.randint(0, I-1)
				if linhasNurse.count(newNurse) == 0:
					linhasNurse.append(newNurse)
		else:
			linhasNurse = [i for i in range(I)]
			
		return linhasNurse, linhasDias

	def simplicaVX(self, schedule):
		output = []
		for day in schedule:
			if sum(day) > 0.5:
				output.append(1)
			else:
				output.append(0)
				
		return output
	
	def add_xRt(self):
		r_t = self.sets.R_t

		T = len(r_t)

		xRt = []
		for before in range(T):
			xRt.append([])
			for after in range(T):
				xRt[-1].append([i for i in [i for i, x in enumerate(r_t[before]) if not x] if i in [i for i, x in enumerate([r_t[i][after] for i in range(len(r_t))]) if not x]])
			xRt[-1].append([i for i, x in enumerate(r_t[before]) if not x])
		xRt.append([])
		for after in range(T):
			xRt[-1].append([i for i, x in enumerate([r_t[i][after] for i in range(len(r_t))]) if not x])
			
		self.sets.xRt = xRt
	
	def run(self, tempo):
		
		getcontext().prec = 15
		tempo = Decimal(tempo)
		tempoTotal = tempo
		
		self.add_xRt()
		sets, parameters = self.sets, self.parameters

		I, D, T, W = len(self.sets.I), len(self.sets.D), len(self.sets.T), len(self.sets.W)
		self.I = I
		self.D = D
		self.T = T
		self.W = W
		m, x, k, y, z, v = self.model.m, self.model.x, self.model.k, self.model.y, self.model.z, self.model.v
		
		started, objVal = self.start(I, D, T, m, x)
		sobjVal = objVal
		
		currentSolution = self.solution
		currentObj = objVal
		bestSolution = self.solution
		bestObj = objVal
		initialSolution = self.solution
		initialObj = objVal
		
		print("START", objVal)
		
		alternate = True
		initialTime = tempo
		#minIters = 5
		maxSolverTime = 12
		maxVNDTime = Decimal(0.8)*initialTime
		maxImprovingTime = Decimal(0.2)*initialTime
		
		# vndModes = ["scrumble"]
		# vndIters = [10000]
		# vndTols = [500]
		# vndWays = ["light"]
		# vndParam = [[100, False]]
		
		vndMode = 0
		first = True
		allowFix = True
		rodadas = 0
		squareSize = 1000
		freeFromWhile = False
		while tempo > maxImprovingTime and not freeFromWhile:
			rodadas += 1
			print("###",rodadas, squareSize)
			#input()
			
			currentSolution = bestSolution
			
			if not first and allowFix:
				###################################START OF MIP TO FIX HIGH PENALITY AND RANDOM PARTS
				logging.info("@!@ FIX HIGH START :"+str(bestObj))
				mipNumIters = min(rodadas, 2*W)
				timesOptimalAndWeel = 0
				for iterador in range(mipNumIters):
					logging.info("@!@ FIX HIGH ("+str(iterador)+") :"+str(bestObj))
					
					if tempo < maxImprovingTime:
						freeFromWhile = True
						break
				
					startTempo = time.time()
					
					mipSeed = random.randint(0,3)
					if mipSeed == 0:
						cotaNurse = min(50, I)
						cotaDias = math.floor(squareSize/cotaNurse)
						linhasNurse, linhasDias = self.pesaSol(currentSolution, 2, 2, max(1, cotaDias - 2*2), cotaNurse)
					elif mipSeed == 1:
						cotaNurse = min(25, math.ceil(0.5*I))
						cotaDias = math.floor(squareSize/cotaNurse)
						linhasNurse, linhasDias = self.pesaSol(currentSolution, 4, 2, max(1, cotaDias - 4*2), cotaNurse)
					elif mipSeed == 2:
						cotaNurse = min(12, math.ceil(0.25*I))
						cotaDias = math.floor(squareSize/cotaNurse)
						linhasNurse, linhasDias = self.pesaSol(currentSolution, 5, 2, max(1, cotaDias - 5*2), cotaNurse)
					else:
						cotaNurse = math.ceil(random.triangular(1, I, 1))
						cotaDias = math.floor(squareSize/cotaNurse)
						linhasNurse, linhasDias = self.pesaSol(currentSolution, 2, 2, max(1, cotaDias - 2*2), cotaNurse)
						
					
					print(linhasNurse)
					print(linhasDias)
					#input()
					
					m.resetParams()
					m.reset(0)
					
					currentSolution = self.fixVarsSol(currentSolution, x, [i for i in range(I)], 0, D)
					
					self.unfixVars(currentSolution, x, linhasNurse, linhasDias)
					
					m.setParam("TimeLimit", min(maxSolverTime, (tempo - maxImprovingTime)))
					m.setParam("MIPFocus", 3)
					m.setParam("PreSolve", 2)
					m.setParam("Cuts", 3)
					if random.randint(0, 1):
						m.setParam("BestObjStop", max(1, math.floor(0.95*bestObj)))
					m.optimize()
					
					status = m.Status
					solnum = m.solCount
					if (status in (GRB.OPTIMAL, GRB.TIME_LIMIT, GRB.SOLUTION_LIMIT, GRB.USER_OBJ_LIMIT)) and solnum > 0:
					
						if status != GRB.TIME_LIMIT:
							squareSize += 10
						else:
							maxSolverTime += 0.2
					
						objVal = m.objVal
						
						logging.info("@#@ FIX HIGH ("+str(iterador)+") :"+str(objVal)+":"+str(bestObj))
							
						currentSolution = self.fixVars(currentSolution, x, linhasNurse, linhasDias)
						
						if objVal <= bestObj:	
							bestSolution = currentSolution
							bestObj = objVal
						
						if status == GRB.OPTIMAL:
							if squareSize > 7*D*I:
								freeFromWhile = True
								break
			
					tempo -= Decimal(time.time() - startTempo)
					logging.info("@@@ FIX HIGH ("+str(iterador)+") :"+str(status)+":"+str(solnum)+":"+str(tempo))
				
				####################################################################################
				print("Finished Fix",objVal)
				logging.info("@$@ FIX HIGH :"+str(objVal)+":"+str(bestObj)+":"+str(tempo))
				
			m.resetParams()
			m.reset(0)
			
			###################################START OF VND
			
			####adicionar aqui o coisinho pra poder fazer um FOR, o move fica do lado de fora
			
			first = False
			
			tentativasFina = 0
			tentativasGeral = 0
			iteracoes = 0
			while tentativasFina < min(rodadas, 20) and tentativasGeral < 1 + min(0.5*rodadas, 9) and iteracoes < 10:
			
				descida = Move()
				descida.herdaSolucao(bestSolution, sets, parameters, self.model)
				descida.settaSolution(bestObj)
				
				iteracoes += 1
				startTempo = time.time()
				
				#deep, nostag, telhado, nostag, ciclo
				#"n-sind", "n-bind", "n-mind", "ns-sind", "ns-bind", "ns-mind", "short-ind", "shorts-ind"
				objVal = descida.run(False, 1000000, min(maxVNDTime, (tempo - maxImprovingTime)), 0, [1000, [200, 100], [1000, 100, 0.994], 1000, [200, 100]], "random", "smart", [50, 30, 20, 40, 20, 15, 50, 25])
				currentSolution = descida.returnSolution()
				
				logging.info("$!$ VND :"+str(objVal)+":"+str(bestObj))
				print("Finish VND", objVal, bestObj)
				
				if objVal < 0.9*bestObj:
					tentativasFina = 0
					tentativasGeral = 0
				elif not objVal < 0.95*bestObj:
					tentativasGeral += 1
				else:
					tentativasFina += 1
				
				if objVal < bestObj:
					bestObj = objVal
					bestSolution = currentSolution
					
				tempo -= Decimal(time.time() - startTempo)
				logging.info("$!$ VND :"+":"+str(bestObj)+":"+str(objVal)+":"+str(tempo))
				
		if tempo > 0 and allowFix:
			logging.info("%!% MIP IMPROVE :"+str(bestObj)+":"+str(tempo))
			
			###################################START OF MIP IMPROVING ALL
			m.resetParams()
			m.reset(0)
			
			self.unfixVars(bestSolution, x, [i for i in range(I)], [d for d in range(D)])
			
			m.setParam("TimeLimit", tempo)
			m.setParam("MIPFocus", 3)
			m.setParam("PreSolve", 2)
			m.setParam("Cuts", 3)
			m.optimize()
			tempo -= Decimal(m.Runtime)
			
			status = m.Status
			solnum = m.solCount
			if (status in (GRB.OPTIMAL, GRB.TIME_LIMIT, GRB.SOLUTION_LIMIT, GRB.USER_OBJ_LIMIT)) and solnum > 0:
				if m.objVal < bestObj:
					bestObj = m.objVal
					bestSolution = self.fixVars(bestSolution, x, [i for i in range(I)], [d for d in range(D)])
			else:
				bestSolution = self.fixVarsSol(bestSolution, x, [i for i in range(I)], 0, D)
			
			####################################################################################
			
			logging.info("%@% MIP IMPROVE :"+str(bestObj)+":"+str(tempo))
		print("TEMPO",tempo)
		
		self.solution = bestSolution
		
		# input()
		return bestObj, tempoTotal - tempo