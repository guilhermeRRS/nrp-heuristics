# coding=utf-8
def update_x(self, nurse, day, newShift):

	self.v_x[nurse][day] = newShift
	
def update_k(self, day, nurse):
	
	week = 0
	if (day + 2) % 7 == 0:
		week = (day + 2) / 7
	elif (day + 1) % 7 == 0:
		week = (day + 1) / 7
	week = int(week) - 1
	
	if week >= 0:
		if self.v_x[nurse][week*7+5] == -1 and self.v_x[nurse][week*7+6] == -1:
			self.v_k[nurse][week] = 0
			
		else:
			self.v_k[nurse][week] = 1
			
def update_yz(self, day, oldShift, newShift):
	
	if oldShift >= 0:
		if self.v_y[day][oldShift] > 0 or self.v_z[day][oldShift] == 0:
			self.v_y[day][oldShift] += 1
		else:
			self.v_z[day][oldShift] -= 1
			
	
	if newShift >= 0:
		if self.v_z[day][newShift] > 0 or self.v_y[day][newShift] == 0:
			self.v_z[day][newShift] += 1
		else:
			self.v_y[day][newShift] -= 1
	
			
def update_nwl(self, nurse, currentShift, newShift):

	newWorkload = self.v_nwl[nurse]
	if currentShift >= 0:
		newWorkload	-= self.parameters.l_t[currentShift]
		
	if newShift >= 0:
		newWorkload += self.parameters.l_t[newShift]
		
	self.v_nwl[nurse] = newWorkload
	
def update_ngs(self, nurse, currentShift, newShift):
	
	if currentShift >= 0:
		self.v_ngs[nurse][currentShift] -= 1
		
	if newShift >= 0:
		self.v_ngs[nurse][newShift] += 1