# coding=utf-8
import os, sys, logging, random, math, time
from decimal import *

def selectNeighbourhood_twoExchange(self, tempo, choosenDay = -1): #não verificada, não utilize (vizinhança abandonada)
	
	I = self.I
	D = self.D
	maxTries = 50000
	
	if not choosenDay < 0:
		day = choosenDay
	
	queueNurse = []
	tries = 0
	while len(queueNurse) == 0 and tempo > 0 and tries < maxTries:
		startTime = time.time()
		
		if choosenDay < 0:
			day = random.randint(0, D-1)
		nurse = random.randint(0, I-1)
		
		while len(queueNurse) == 0:
			
			nextNurse = random.randint(0, I-1)
			if queueNurse.count(nextNurse) == 0 and nurse != nextNurse:
				queueNurse.append(nextNurse)
				
		for i in range(1):
			if not self.validMove_twoExchange(nurse, queueNurse[i], self.v_x[nurse], self.v_x[queueNurse[i]], day, True):
				del queueNurse[i]
				
		tempo -= Decimal(time.time() - startTime)
		tries += 1
		
		if len(queueNurse) > 0:
			break
			
		#if tries % 100 == 0:
		#	print("@ "+str(tries))
	
	if not tries < maxTries:
		if len(queueNurse) == 0:
			return -1, [], -1
	
	if tempo > 0:
		return nurse, queueNurse[i], day
	else:
		return -1, [], -1
		
def selectNeighbourhood_twoExchange_varrer(self, tempo, objVal, choosenDay = -1): #não verificada, não utilize (vizinhança abandonada)
	
	I = self.I
	D = self.D
	maxTries = 50000
	
	if not choosenDay < 0:
		day = choosenDay
	
	queueNurse = []
	tries = 0
	while len(queueNurse) == 0 and tempo > 0 and tries < maxTries:
		startTime = time.time()
		
		if choosenDay < 0:
			day = random.randint(0, D-1)
		nurse = random.randint(0, I-1)
		
		while len(queueNurse) < I - 1:
			
			nextNurse = random.randint(0, I-1)
			if queueNurse.count(nextNurse) == 0 and nurse != nextNurse:
				queueNurse.append(nextNurse)
				
		for i in range(I-2, -1, -1):
			if not self.validMove_twoExchange(nurse, queueNurse[i], self.v_x[nurse], self.v_x[queueNurse[i]], day, True):
				del queueNurse[i]
				
		tempo -= Decimal(time.time() - startTime)
		tries += 1
		
		if len(queueNurse) > 0:
			break
			
		#if tries % 100 == 0:
		#	print("@ "+str(tries))
	
	if not tries < maxTries:
		if len(queueNurse) == 0:
			return -1, [], -1
	
	if tempo > 0:
		
		##aqui começa a varredura
		bestMove = -1
		bestObj = -1
		nurse1Shift = self.v_x[nurse][day]
		for i in range(len(queueNurse)):
			nurse2Shift = self.v_x[queueNurse[i]][day]
			objVal = self.estimateMove_twoExchange(nurse, queueNurse[i], nurse1Shift, nurse2Shift, day, objVal)
			if bestObj > objVal or bestObj == -1:
				bestObj = objVal
				bestMove = i
				
		nurse2 = queueNurse[bestMove]
		
		return nurse, nurse2, day
	else:
		return -1, [], -1

def selectNeighbourhood_threeExchange(self, tempo, choosenDay = -1): #não verificada, não utilize (vizinhança abandonada)
	
	I = self.I
	D = self.D
	maxTries = 50000
	
	if not choosenDay < 0:
		day = choosenDay
				
	queueNurse = []
	queueShifts = []
	
	tries = 0
	while tempo > 0 and tries < maxTries:
		
		startTime = time.time()
		
		queueNurse = []
		queueShifts = []
		
		if choosenDay < 0:
			day = random.randint(0, D-1)
		
		maxNurses = min(random.randint(3, 5), max(2, I-2))
		failed = False
		while len(queueNurse) < maxNurses and not failed:
			while True:
				nurse = random.randint(0, I-1)
				if queueNurse.count(nurse) == 0:
					queueNurse.append(nurse)
					queueShifts.append(self.v_x[nurse][day])
					break
			
			if len(queueNurse) > 1:
				if not self.validMove_singular(nurse, self.v_x[nurse], day, queueShifts[-2], True):
					failed = True
					
		if not failed:
			nurse = queueNurse[0]
			if self.validMove_singular(nurse, self.v_x[nurse], day, queueShifts[-1], True):
				return queueNurse, [queueShifts[-1]] + queueShifts[:-1], day
		
		tempo -= Decimal(time.time() - startTime)
		tries += 1
		
	if not tries < maxTries:
		if len(queueNurse) == 0:
			return [], [], -1
	
	if tempo > 0:
		return queueNurse, queueShifts, day
	else:
		return [], [], -1

def selectNeighbourhood_doubleExchange(self, tempo, choosenDay = -1): #não verificada, não utilize (vizinhança abandonada)
	
	I = self.I
	D = self.D
	maxTries = 50000
	
	if not choosenDay < 0:
		day = choosenDay
	
	queueNurse = []
	tries = 0
	while len(queueNurse) == 0 and tempo > 0 and tries < maxTries:
		startTime = time.time()
		
		if choosenDay < 0:
			day = random.randint(0, D-2)
		nurse = random.randint(0, I-1)
		
		while len(queueNurse) == 0:
			
			nextNurse = random.randint(0, I-1)
			if queueNurse.count(nextNurse) == 0 and nurse != nextNurse:
				queueNurse.append(nextNurse)
				
		for i in range(1):
			if not self.validMove_doubleExchange(nurse, queueNurse[i], self.v_x[nurse], self.v_x[queueNurse[i]], day, True):
				del queueNurse[i]
				
		tempo -= Decimal(time.time() - startTime)
		tries += 1
		
		if len(queueNurse) > 0:
			break
			
		#if tries % 100 == 0:
		#	print("@ "+str(tries))
	
	if not tries < maxTries:
		if len(queueNurse) == 0:
			return -1, [], -1
	
	if tempo > 0:
		return nurse, queueNurse[0], day
	else:
		return -1, [], -1
		
def selectNeighbourhood_doubleExchange_varrer(self, tempo, objVal, choosenDay = -1): #não verificada, não utilize (vizinhança abandonada)
	
	I = self.I
	D = self.D
	maxTries = 50000
	
	if not choosenDay < 0:
		day = choosenDay
	
	queueNurse = []
	tries = 0
	while len(queueNurse) == 0 and tempo > 0 and tries < maxTries:
		startTime = time.time()
		
		if choosenDay < 0:
			day = random.randint(0, D-2)
		nurse = random.randint(0, I-1)
		
		while len(queueNurse) < I - 1:
			
			nextNurse = random.randint(0, I-1)
			if queueNurse.count(nextNurse) == 0 and nurse != nextNurse:
				queueNurse.append(nextNurse)
				
		for i in range(I-2, -1, -1):
			if not self.validMove_doubleExchange(nurse, queueNurse[i], self.v_x[nurse], self.v_x[queueNurse[i]], day, True):
				del queueNurse[i]
				
		tempo -= Decimal(time.time() - startTime)
		tries += 1
		
		if len(queueNurse) > 0:
			break
			
		#if tries % 100 == 0:
		#	print("@ "+str(tries))
	
	if not tries < maxTries:
		if len(queueNurse) == 0:
			return -1, [], -1
	
	if tempo > 0:
	
		##aqui começa a varredura
		bestMove = -1
		bestObj = -1
		nurse1Schedule = self.v_x[nurse]
		for i in range(len(queueNurse)):
			nurse2Schedule = self.v_x[queueNurse[i]]
			objVal = self.estimateMove_doubleExchange(day, nurse, queueNurse[i], nurse1Schedule, nurse2Schedule, objVal)
			if bestObj > objVal or bestObj == -1:
				bestObj = objVal
				bestMove = i
				
		nurse2 = queueNurse[bestMove]
		
		return nurse, nurse2, day
	else:
		return -1, [], -1

def selectNeighbourhood_multiExchange(self, tempo): #não verificada, não utilize (vizinhança abandonada)
	
	I = self.I
	D = self.D
	maxTries = 50000
	
	queueNurse = []
	days = []
	tries = 0
	while len(queueNurse) == 0 and tempo > 0 and tries < maxTries:
		startTime = time.time()
		
		days = []
		while len(days) < D:
			day = random.randint(0, D-1)
			if days.count(day) == 0:
				days.append(day)
			if len(days) > 2:
				if random.randint(0, 1):
					break
				
		nurse = random.randint(0, I-1)
		
		while len(queueNurse) == 0:
			
			nextNurse = random.randint(0, I-1)
			if queueNurse.count(nextNurse) == 0 and nurse != nextNurse:
				queueNurse.append(nextNurse)
				
		for i in range(1):
			if not self.validMove_multiExchange(nurse, queueNurse[i], self.v_x[nurse], self.v_x[queueNurse[i]], days, True):
				del queueNurse[i]
				
		tempo -= Decimal(time.time() - startTime)
		tries += 1
		
		if len(queueNurse) > 0:
			break
			
		#if tries % 100 == 0:
		#	print("@ "+str(tries))
	
	if not tries < maxTries:
		if len(queueNurse) == 0:
			return -1, [], []
	
	if tempo > 0:
		return nurse, queueNurse[0], days
	else:
		return -1, [], []

def selectNeighbourhood_multiExchange_varrer(self, tempo, objVal): #não verificada, não utilize (vizinhança abandonada)
	
	I = self.I
	D = self.D
	maxTries = 50000
	
	queueNurse = []
	days = []
	tries = 0
	while len(queueNurse) == 0 and tempo > 0 and tries < maxTries:
		startTime = time.time()
		
		days = []
		while len(days) < D:
			day = random.randint(0, D-1)
			if days.count(day) == 0:
				days.append(day)
			if len(days) > 2:
				if random.randint(0, 1):
					break
				
		nurse = random.randint(0, I-1)
		
		while len(queueNurse) < I - 1:
			
			nextNurse = random.randint(0, I-1)
			if queueNurse.count(nextNurse) == 0 and nurse != nextNurse:
				queueNurse.append(nextNurse)
				
		for i in range(I-2, -1, -1):
			if not self.validMove_multiExchange(nurse, queueNurse[i], self.v_x[nurse], self.v_x[queueNurse[i]], days, True):
				del queueNurse[i]
				
		tempo -= Decimal(time.time() - startTime)
		tries += 1
		
		if len(queueNurse) > 0:
			break
			
		#if tries % 100 == 0:
		#	print("@ "+str(tries))
	
	if not tries < maxTries:
		if len(queueNurse) == 0:
			return -1, [], []
	
	if tempo > 0:
	
		##aqui começa a varredura
		bestMove = -1
		bestObj = -1
		
		for i in range(len(queueNurse)):
			objVal = self.estimateMove_multiExchange(nurse, queueNurse[i], days, objVal)
			if bestObj > objVal or bestObj == -1:
				bestObj = objVal
				bestMove = i
				
		nurse2 = queueNurse[bestMove]
	
		return nurse, nurse2, days
	else:
		return -1, [], []

def selectNeighbourhood_blockExchange(self, tempo): #não verificada, não utilize (vizinhança abandonada)
	
	I = self.I
	D = self.D
	maxTries = 50000
	lengthBlock = 3
	
	queueNurse = []
	tries = 0
	while len(queueNurse) == 0 and tempo > 0 and tries < maxTries:
		startTime = time.time()
		
		lengthBlock = 3
		while lengthBlock < D-1:
			if random.randint(0, 1):
				break
			lengthBlock += 1
		day = random.randint(0, D-lengthBlock)
		nurse = random.randint(0, I-1)
		
		while len(queueNurse) == 0:
			
			nextNurse = random.randint(0, I-1)
			if queueNurse.count(nextNurse) == 0 and nurse != nextNurse:
				queueNurse.append(nextNurse)
				
		for i in range(1):
			if not self.validMove_blockExchange(nurse, queueNurse[i], self.v_x[nurse], self.v_x[queueNurse[i]], day, lengthBlock, True):
				del queueNurse[i]
				
		tempo -= Decimal(time.time() - startTime)
		tries += 1
		
		if len(queueNurse) > 0:
			break
			
		#if tries % 100 == 0:
		#	print("@ "+str(tries))
	
	if not tries < maxTries:
		if len(queueNurse) == 0:
			return -1, [], -1, -1
	
	if tempo > 0:
		return nurse, queueNurse[0], day, lengthBlock
	else:
		return -1, [], -1, -1

def selectNeighbourhood_blockExchange_varrer(self, tempo, objVal): #não verificada, não utilize (vizinhança abandonada)
	
	I = self.I
	D = self.D
	maxTries = 50000
	lengthBlock = 3
	
	queueNurse = []
	tries = 0
	while len(queueNurse) == 0 and tempo > 0 and tries < maxTries:
		startTime = time.time()
		
		lengthBlock = 3
		while lengthBlock < D-1:
			if random.randint(0, 1):
				break
			lengthBlock += 1
		day = random.randint(0, D-lengthBlock)
		nurse = random.randint(0, I-1)
		
		while len(queueNurse) < I - 1:
			
			nextNurse = random.randint(0, I-1)
			if queueNurse.count(nextNurse) == 0 and nurse != nextNurse:
				queueNurse.append(nextNurse)
				
		for i in range(I-2, -1, -1):
			if not self.validMove_blockExchange(nurse, queueNurse[i], self.v_x[nurse], self.v_x[queueNurse[i]], day, lengthBlock, True):
				del queueNurse[i]
				
		tempo -= Decimal(time.time() - startTime)
		tries += 1
		
		if len(queueNurse) > 0:
			break
			
		#if tries % 100 == 0:
		#	print("@ "+str(tries))
	
	if len(queueNurse) > 0:
		
		##aqui começa a varredura
		bestMove = -1
		bestObj = -1
		nurse1Schedule = self.v_x[nurse]
		for i in range(len(queueNurse)):
			nurse2Schedule = self.v_x[queueNurse[i]]
			objVal = self.estimateMove_blockExchange(nurse, queueNurse[i], day, lengthBlock, objVal)
			if bestObj > objVal or bestObj == -1:
				bestObj = objVal
				bestMove = i
				
		nurse2 = queueNurse[bestMove]
	
		return nurse, queueNurse[0], day, lengthBlock
	else:
		return -1, [], -1, -1

def selectNeighbourhood_groupNind(self, tempo, mode):
	
	if not mode in ("n-sind","n-mind","n-bind"):
		return -1, [], []
	
	I = self.I
	D = self.D
	maxTries = 1000
	
	nurse = -1
	tries = 0
	while nurse == -1 and tempo > 0 and tries < maxTries:
		startTime = time.time()
		
		nurse = random.randint(0, I-1)
		
		if mode == "n-sind":
			lengthBlock = 1
		else:
			lengthBlock = random.randint(2, self.parameters.c_max[nurse])
		
		days = []
		changes = []
		localTries = 0
		while len(days) < lengthBlock and localTries < 2*D:
			localTries += 1
			day = random.randint(0, D-lengthBlock)
			if days.count(day) == 0:
				shift = self.v_x[nurse][day]
				if shift >= 0:
					before = -1 if day - 1 < 0 else self.v_x[nurse][day-1]
					after = -1 if day + 1 > D-1 else self.v_x[nurse][day+1]
					if mode == "n-sind" or mode == "n-bind":
						days.append(day)
						if mode == "n-sind":
							changes.append(random.choice(self.sets.xRt[before][after]))
					elif mode == "n-mind":
						if days.count(day-1) > 0:
							before = changes[days.index(day-1)]
						if days.count(day+1) > 0:
							after = changes[days.index(day+1)]
						if len(self.sets.xRt[before][after]) > 0:
							days.append(day)
							changes.append(random.choice(self.sets.xRt[before][after]))
		
		if mode == "n-bind" and len(days) > 0:
			day = days[0]
			days = []
			before = -1 if day - 1 < 0 else self.v_x[nurse][day-1]
			after = -1 if day + 1 > D-1 else self.v_x[nurse][day+1]
			for d in range(day, day+lengthBlock):
				if len(self.sets.xRt[before][after]) == 0:
					break
				days.append(d)
				changes.append(random.choice(self.sets.xRt[before][after]))
				before = changes[-1]
				after = -1 if d + 2 > D-1 else self.v_x[nurse][d+2]
		
		if len(days) > 0:
			if not self.validMove_groupNind(nurse, days, changes, self.v_x[nurse]):
				nurse = -1
		else:
			nurse = -1
				
		tempo -= Decimal(time.time() - startTime)
		tries += 1
			
		#if tries % 100 == 0:
		#	print("@ "+str(tries))
		
	if nurse >= 0:
		return nurse, days, changes
	else:
		return -1, [], []

def getMaiorCmax(self):
	maior = self.parameters.c_max[0]
	for i in self.parameters.c_max:
		if i > maior:
			maior = i
	return max(2, maior)

def selectNeighbourhood_groupNSind(self, tempo, mode):
	
	if not mode in ("ns-sind","ns-mind","ns-bind"):
		return [], [], []
	
	I = self.I
	D = self.D
	maxTries = 1000
	
	nurses = []
	tries = 0
	maiorCmax = self.getMaiorCmax()
	while len(nurses) == 0 and tempo > 0 and tries < maxTries:
		startTime = time.time()
		
		lengthNurses = random.randint(1, I-1)
		queuenurses = [i for i in range(I)]
		random.shuffle(queuenurses)
		
		if mode == "ns-sind":
			lengthBlock = 1
		else:
			lengthBlock = random.randint(2, maiorCmax)
		
		days = []
		nurse = queuenurses[0]
		localTries = 0
		while len(days) < lengthBlock and localTries < 2*D:
			localTries += 1
			day = random.randint(0, D-lengthBlock)
			if days.count(day) == 0:
				shift = self.v_x[nurse][day]
				if shift >= 0:
					days.append(day)
		
		if mode == "ns-bind" and len(days) > 0:
			day = days[0]
			days = []
			for d in range(day, day+lengthBlock):
				days.append(d)
		
		if len(days) > 0:
			lengthBlock = len(days)
			changes = []
			nurses = []
			i = 0
			while len(nurses) < lengthNurses and i < I:
				
				nurse = queuenurses[i]
				
				tmpchanges = []
				for d in range(lengthBlock):
					tmpchanges.append(random.randint(0, self.T-1))
			
				if self.validMove_groupNind(nurse, days, tmpchanges, self.v_x[nurse]):
					changes.append(tmpchanges)
					nurses.append(nurse)
				i += 1
		else:
			nurse = -1
				
		tempo -= Decimal(time.time() - startTime)
		tries += 1
			
		#if tries % 100 == 0:
		#	print("@ "+str(tries))
		
	if len(nurses) > 0:
		return nurses, days, changes
	else:
		return [], [], []

def selectNeighbourhood_shortInd(self, tempo):
	
	I = self.I
	D = self.D
	maxTries = 1000
	maxLength = 10#repare que este parâmetro se for muito pequeno impede que sejam feitos movimentos depenentes de apagar intervalos (c_max) /criar novos (c_min) ->queremos movimentos pequenos, mas, supondo desconhecimento desses parâmetros, deixamos a cargo do componente aleatório a decisão de prolongar ou não (tendendo a prolongar o mínimo possível)
	lengthBlock = maxLength
	
	#repare que há uma grande parametrização "hardcoded"
		#diminuição de longos intervalos de folga para tentar equilibrar com a pequena quantidade de novos intervalos de trabalho (a ideia deste movimento não é apagar jornadas, sendo assim, busca-se um balanço nos dois tipos de movimento)
	
	nurse = -1
	tries = 0
	while nurse == -1 and tempo > 0 and tries < maxTries:
		startTime = time.time()
		lengthBlock = random.randint(2, maxLength)
		day = random.randint(0, D-lengthBlock)
		nurse = random.randint(0, I-1)
		shift = self.v_x[nurse][day]
		
		changes = []
		before = -1 if day - 1 < 0 else self.v_x[nurse][day-1]
		after = -1 if day + 1 > D-1 else self.v_x[nurse][day+1]
		if random.randint(0, 10):
			for i in range(lengthBlock):
				if len(self.sets.xRt[before][after]) == 0:
					break
				changes.append(random.choice(self.sets.xRt[before][after]))
				before = changes[-1]
				after = -1 if day + i + 2 > D-1 else self.v_x[nurse][day + i+2]
		else:
			for i in range(lengthBlock):
				changes.append(-1)
		
		if not self.validMove_shortInd(nurse, day, changes, self.v_x[nurse]):
			nurse = -1
				
		tempo -= Decimal(time.time() - startTime)
		tries += 1
			
		#if tries % 100 == 0:
		#	print("@ "+str(tries))
		
	if nurse >= 0:
		return nurse, day, changes
	else:
		return -1, -1, []
		
def selectNeighbourhood_shortsInd(self, tempo):
	I = self.I
	D = self.D
	maxTries = 1000
	
	nurses = []
	days = []
	changes = []
	tries = 0
	while len(nurses) == 0 and tempo > 0 and tries < maxTries:
		
		lengthNurses = random.randint(1, min(10, I-1))
		nurses = []
		days = []
		changes = []
		localTries = 0
		while len(nurses) < lengthNurses and localTries < 100:
			localTries += 1
			startTime = time.time()
			
			rcv_nurse, rcv_day, rcv_changes = self.selectNeighbourhood_shortInd(tempo)
			if rcv_nurse >= 0:
				if nurses.count(rcv_nurse) == 0:
					nurses.append(rcv_nurse)
					days.append(rcv_day)
					changes.append(rcv_changes)
			
			tempo -= Decimal(time.time() - startTime)
		
		tries += 1
	
	if len(nurses) > 0:
		return nurses, days, changes
	else:
		return [], [], []

def simplicaSchedule(self, schedule):
	output = []
	for day in schedule:
		if day >= 0:
			output.append(1)
		else:
			output.append(0)
			
	return output