# coding=utf-8
import random, math

#def constraint1 #not needed

def constraint2(self, nurse, shiftBefore, shiftAfter):
	
	if shiftBefore < 0 or shiftAfter < 0:
		return True
		
	return not self.sets.R_t[shiftBefore][shiftAfter]
	
def constraint3(self, nurse, shift, currentShift):
	return (self.v_ngs[nurse][shift] + 1 <= self.parameters["m_max"][nurse][shift]) or shift == currentShift

def constraint3_multi(self, nurse, oldShifts, newShifts):
	ngs = self.v_ngs[nurse].copy()
	
	for shift in oldShifts:
		if shift >= 0:
			ngs[shift] -= 1
	for shift in newShifts:
		if shift >= 0:
			ngs[shift] += 1
			
	for t in range(self.T):
		if ngs[t] > self.parameters.m_max[nurse][t]:
			return False
	return True

def constraint45(self, nurse, currentShift, newShift):
	
	newWorkload = self.v_nwl[nurse]
	if currentShift >= 0:
		newWorkload	-= self.parameters.l_t[currentShift]
	if newShift >= 0:
		newWorkload += self.parameters.l_t[newShift]
	if newWorkload < self.parameters.b_min[nurse] or newWorkload > self.parameters["b_max"][nurse]:
		return False
	return True

def constraint45_multi(self, nurse, oldShifts, newShifts):
	
	newWorkload = self.v_nwl[nurse]
	for i in range(len(oldShifts)):
		if oldShifts[i] >= 0:
			newWorkload	-= self.parameters.l_t[oldShifts[i]]
		if newShifts[i] >= 0:
			newWorkload += self.parameters.l_t[newShifts[i]]
	if newWorkload < self.parameters.b_min[nurse] or newWorkload > self.parameters.b_max[nurse]:
		return False
	return True

def getFreeInterval(self, nurse, schedule, day, simplified = False):
	
	D = self.D
	startInt = day
	
	while startInt >= 0:
		if schedule[startInt] < 0:
			startInt -= 1
		else:
			startInt += 1
			break
			
	if startInt < 0:
		startInt = 0
	
	endInt = day
	
	while endInt <= D-1:
		if schedule[endInt] < 0:
			endInt += 1
		else:
			endInt -= 1
			break
		
	if endInt > D-1:
		endInt = D-1
	
	if simplified:
		return endInt - startInt + 1
		
	return startInt, endInt, endInt - startInt + 1

def getWorkingInterval(self, nurse, schedule, day, simplified = False):
	
	D = self.D
	startInt = day
	
	while startInt >= 0:
		if schedule[startInt] >= 0:
			startInt -= 1
		else:
			startInt += 1
			break
			
	if startInt < 0:
		startInt = 0
	
	endInt = day
	
	while endInt <= D-1:
		if schedule[endInt] >= 0:
			endInt += 1
		else:
			endInt -= 1
			break
		
	if endInt > D-1:
		endInt = D-1
	
	if simplified:
		return endInt - startInt + 1
	
	return startInt, endInt, endInt - startInt + 1

def constraint678_free(self, nurse, schedule, day): #working - free - working
	
	D = self.D
	start, end, size = self.getFreeInterval(nurse, schedule, day)
	
	if size < self.parameters.o_min[nurse]:
		return False
	
	if start > 0:
		if not (self.getWorkingInterval(nurse, schedule, start-1, True) >= self.parameters.c_min[nurse] or start-1 == 0):
			return False
			
	if end < D-1:
		if not (self.getWorkingInterval(nurse, schedule, end+1, True) >= self.parameters.c_min[nurse] or end+1 == D-1):
			return False
			
	return True

def constraint678_work(self, nurse, schedule, day): #free - working - free

	D = self.D
	start, end, size = self.getWorkingInterval(nurse, schedule, day)
	
	if size < self.parameters.c_min[nurse] or size > self.parameters.c_max[nurse]:
		return False
		
	if start > 0:
		if not (self.getFreeInterval(nurse, schedule, start-1, True) >= self.parameters.o_min[nurse] or start-1 == 0):
			return False
			
	if end < D-1:
		if not (self.getFreeInterval(nurse, schedule, end+1, True) >= self.parameters.o_min[nurse] or end+1 == D-1):
			return False
	return True

def constraint678(self, nurse, schedule, day):
	
	shift = schedule[day]
	if shift < 0:
		return self.constraint678_free(nurse, schedule, day)
	else:
		return self.constraint678_work(nurse, schedule, day)

def constraint8(self, nurse, schedule, day):
	if day == 0:
		back = day
	else:
		back = day - 1
		while back >= 0:
			if schedule[back] >= 0:
				back += 1
				break
			back -= 1
		if back < 0:
			back = 0
	
	if day == self.D - 1:
		end = day
	else:
		end = day + 1
		while end < self.D:
			if schedule[end] >= 0:
				end -= 1
				break
			end += 1
		if end > self.D - 1:
			end = self.D - 1
			
	return end == self.D - 1 or back == 0 or end - back + 1 >= self.parameters["o_min"][nurse]

def constraint9(self, nurse, day, shift = -1):
	
	if shift >= 0:
		return True
		
	if sum(self.v_k[nurse]) <= self.parameters["a_max"][nurse]:
		return True
	
	if (day + 2) % 7 or (day + 1) % 7:
		return False

def constraint9_multi(self, schedule, nurse, days):
	
	v_k = self.v_k[nurse].copy()
	
	for i in range(len(days)):
		day = days[i]
		week = 0
		if (day + 2) % 7 == 0:
			week = (day + 2) / 7
		elif (day + 1) % 7 == 0:
			week = (day + 1) / 7
		week -= 1
		week = int(week)
		
		if week >= 0:
			if schedule[week*7+5] == -1 and schedule[week*7+6] == -1:
				v_k[week] = 0
				
			else:
				v_k[week] = 1
		
	if sum(v_k) <= self.parameters.a_max[nurse]:
		return True
	
	return False
		
def constraint10(self, nurse, day): #day sempre é um dia de trabalho
	return self.sets.N_i[nurse].count(day) == 0