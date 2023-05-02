# coding=utf-8
import random, math, copy
	
def validMultiShift(self, nurse, schedule, shiftsDays):
	
	schedule = schedule.copy()
	
	modifiedDays = []
	oldShifts = []
	newShifts = []
	for shiftDay in shiftsDays:
		modifiedDays.append(shiftDay[0])
		oldShifts.append(schedule[shiftDay[0]])
		schedule[shiftDay[0]] = shiftDay[1]
		newShifts.append(shiftDay[1])
	lenModifiedDays = len(modifiedDays)
	
	###aplicamos a restrição 2 para todos os dias que sofreram modificação
	for i in range(lenModifiedDays):
		day = modifiedDays[i]
		shift = newShifts[i]
		if shift >= 0:
			if day > 0:
				if not self.constraint2(nurse, schedule[day-1], shift):
					return False
			if day < self.D - 1:
				if not self.constraint2(nurse, shift, schedule[day+1]):
					return False
	
	###aplicamos a restrição 3 para mudanças múltiplas
	if not self.constraint3_multi(nurse, oldShifts, newShifts):
		return False
		
	###aplicamos a restrição 4 e 5 para mudanças múltiplas
	if not self.constraint45_multi(nurse, oldShifts, newShifts):
		return False
	
	###aplicamos a restrição 9
	if not self.constraint9_multi(schedule, nurse, modifiedDays):
		return False
	
	###aplicamos a restrição 10
	for i in range(lenModifiedDays):
		if newShifts[i] >= 0:
			if not self.constraint10(nurse, modifiedDays[i]):
				return False
	
	###aplicamos as restrições de mínimo e máximo (6, 7, 8)
	for i in range(lenModifiedDays):
		if not self.constraint678(nurse, schedule, modifiedDays[i]):
			return False
			
	return True

def cleanNurseMoveEstimative(self, day, nurse, nurseShift, obj):
	if nurseShift >= 0:
		obj += self.parameters.q[nurse][day][nurseShift]
		obj -= self.parameters.p[nurse][day][nurseShift]
	return obj
	
def setNurseMoveEstimative(self, day, nurse, nurseShift, newObj):
	if nurseShift >= 0:
		newObj -= self.parameters.q[nurse][day][nurseShift]
		newObj += self.parameters.p[nurse][day][nurseShift]
	return newObj
	
def estimate_demanda_singleNurse(self, day, oldShift, newShift, newObj):

	if oldShift != newShift:
		if oldShift >= 0:
			if self.v_y[day][oldShift] > 0 or self.v_z[day][oldShift] == 0:
				newObj += self.parameters.w_min[day][oldShift]
			else:
				newObj -= self.parameters.w_max[day][oldShift]
		
		if newShift >= 0:
			if self.v_z[day][newShift] > 0 or self.v_y[day][newShift] == 0:
				newObj += self.parameters.w_max[day][newShift]
			else:
				newObj -= self.parameters.w_min[day][newShift]
			
	return newObj
	
def estimate_demanda_manyNurse(self, day, oldShifts, newShifts, newObj):
	
	v_y = copy.deepcopy(self.v_y[day])
	v_z = copy.deepcopy(self.v_z[day])
	
	for p in range(len(oldShifts)):
		oldShift = oldShifts[p]
		newShift = newShifts[p]
		if oldShift!= newShift:
			if oldShift >= 0:
				if v_y[oldShift] > 0 or v_z[oldShift] == 0:
					newObj += self.parameters.w_min[day][oldShift]
					v_y[oldShift] += 1
				else:
					v_z[oldShift] -= 1
					newObj -= self.parameters.w_max[day][oldShift]
			
			if newShift >= 0:
				if v_z[newShift] > 0 or v_y[newShift] == 0:
					newObj += self.parameters.w_max[day][newShift]
					v_z[newShift] += 1
				else:
					v_y[newShift] -= 1
					newObj -= self.parameters.w_min[day][newShift]
	
	return newObj

def validMove_singular(self, nurse, schedule, day, newShift, forced = False):
	
	nurseShift = schedule[day]
	
	if nurseShift == newShift and forced:
		return False #useless move
	
	if not self.validMultiShift(nurse, schedule, [[day, newShift]]):
		#print("!",day, nurse1, nurse2)
		#print(self.validMultiShift(nurse1, schedule1, [[day, nurse2Shift]]))
		#print(self.validMultiShift(nurse2, schedule2, [[day, nurse1Shift]]))
		#input("@\n")
		return False
		
	return True

def validMove_groupNind(self, nurse, days, newShifts, schedule):
	
	if nurse < 0 or len(newShifts) == 0:
		return False
		
	changes = []
	for i in range(len(newShifts)):
		changes.append([days[i], newShifts[i]])
		
	return self.validMultiShift(nurse, schedule, changes)

def estimateMove_groupNind(self, nurse, days, changes, objVal):

	for i in range(len(changes)):
		
		currentShift = self.v_x[nurse][days[i]]
		objVal = self.cleanNurseMoveEstimative(days[i], nurse, currentShift, objVal)
		objVal = self.setNurseMoveEstimative(days[i], nurse, changes[i], objVal)
		
		objVal = self.estimate_demanda_singleNurse(days[i], currentShift, changes[i], objVal)
	
	return objVal
	
def applyMove_groupNind(self, nurse, days, changes):
	
	for i in range(len(changes)):
		oldShift = self.v_x[nurse][days[i]]
	
		self.update_yz(days[i], oldShift, changes[i])
		self.update_x(nurse, days[i], changes[i])
	
		self.update_k(days[i], nurse)
	
		self.update_nwl(nurse, oldShift, changes[i])
		self.update_ngs(nurse, oldShift, changes[i])

def estimateMove_groupNSind(self, nurses, days, changes, objVal):
	
	for d in range(len(days)):
		
		oldShifts = []
		newShifts = []
		for i in range(len(nurses)):
			
			nurse = nurses[i]
			currentShift = self.v_x[nurse][days[d]]
			objVal = self.cleanNurseMoveEstimative(days[d], nurse, currentShift, objVal)
			objVal = self.setNurseMoveEstimative(days[d], nurse, changes[i][d], objVal)
			
			oldShifts.append(currentShift)
			newShifts.append(changes[i][d])
		
		objVal = self.estimate_demanda_manyNurse(days[d], oldShifts, newShifts, objVal)
	
	return objVal

def validMove_shortInd(self, nurse, day, newShifts, schedule):
	
	if nurse < 0 or len(newShifts) == 0:
		return False
		
	changes = []
	for i in range(len(newShifts)):
		changes.append([day+i, newShifts[i]])
		
	return self.validMultiShift(nurse, schedule, changes)

def estimateMove_shortInd(self, nurse, day, changes, objVal):

	for i in range(len(changes)):
		
		currentShift = self.v_x[nurse][day+i]
		objVal = self.cleanNurseMoveEstimative(day+i, nurse, currentShift, objVal)
		objVal = self.setNurseMoveEstimative(day+i, nurse, changes[i], objVal)
		
		objVal = self.estimate_demanda_singleNurse(day+i, currentShift, changes[i], objVal)
	
	return objVal
	
def applyMove_shortInd(self, nurse, day, changes):
	
	oldShifts = []
	
	for i in range(len(changes)):
		oldShift = self.v_x[nurse][day+i]
	
		self.update_yz(day+i, oldShift, changes[i])
		self.update_x(nurse, day+i, changes[i])
	
		self.update_k(day+i, nurse)
	
		self.update_nwl(nurse, oldShift, changes[i])
		self.update_ngs(nurse, oldShift, changes[i])

def estimateMove_shortsInd(self, nurses, days, changes, objVal):
	
	day_old = []
	day_new = []
	for d in range(self.D):
		day_old.append([])
		day_new.append([])
	
	for i in range(len(nurses)):
		nurse = nurses[i]
		day = days[i]
		mudancas = changes[i]
		for j in range(len(mudancas)):
			
			currentShift = self.v_x[nurse][day+j]
			objVal = self.cleanNurseMoveEstimative(day+j, nurse, currentShift, objVal)
			objVal = self.setNurseMoveEstimative(day+j, nurse, mudancas[j], objVal)
			
			day_old[day+j].append(currentShift)
			day_new[day+j].append(mudancas[j])
			
	for d in range(self.D):
		if len(day_new) > 0:
			objVal = self.estimate_demanda_manyNurse(d, day_old[d], day_new[d], objVal)
	
	return objVal
	
def applyMove_shortsInd(self, nurses, days, changes):
	
	for i in range(len(nurses)):
		nurse = nurses[i]
		day = days[i]
		
		oldShifts = []
		
		mudancas = changes[i]
		for j in range(len(mudancas)):
			oldShift = self.v_x[nurse][day+j]
		
			self.update_yz(day+j, oldShift, mudancas[j])
			self.update_x(nurse, day+j, mudancas[j])
		
			self.update_k(day+j, nurse)
		
			self.update_nwl(nurse, oldShift, mudancas[j])
			self.update_ngs(nurse, oldShift, mudancas[j])