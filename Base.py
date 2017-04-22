

class Person:
	#NumberToDay binding of values.
	NumberToDay = {1 : "Monday", 2 : "Tuesday", 3 : "Wednesday", 4 : "Thursday", 5 : "Friday", 6 : "Saturday", 7 : "Sunday"}

	def __init__(self, name):
		self.name = name
		self.classTypes = [] #A list of possible class types
		self.availableTimes = {1 : [], 2 : [], 3 : [], 4 : [], 5 : [], 6 : [], 7 : []} #The available times as a dictionary w/ a mapping of day to a list of times
		# 1 = Monday, 2 = Tuesday, ... ,7 = sunday


	def addTime(self, day, time):
		# Adds a time that they can play on day and time.
		self.availableTimes[day].append(time)

	def addClass(self, classType):
		# Adds a class to their classes
		if classType == "All":
			self.classTypes.append("Tank")
			self.classTypes.append("Healer")
			self.classTypes.append("DPS")
		else:
			self.classTypes.append(classType)


	def __str__(self):
		#Grab the name
		name = self.name

		#Grab the classTypes
		classTypes = ""
		for i in self.classTypes:
			classTypes = classTypes + i + ", "

		#Grab everything but the last two elements. The last ", " is removed
		classTypes = classTypes[:-2]

		#Grab the day and the times available.
		dayTimes = ""
		for i in range(7):
			j = i + 1
			k = self.NumberToDay[j]
			k = k + ":"
			for ii in self.availableTimes[j]:
				k = k + " " + str(ii)
			k = k + "\n"
			dayTimes = dayTimes + k
		dayTimes = dayTimes[:-1]
		return (name +": " + classTypes + "\n\n" + dayTimes+"\n")
