from Base import *
from itertools import *

def getAllHealers(People):
	'''
	list of People -> list of People

	Takes the entire list of people, filter by if they are a healer
	'''
	compatible = []
	for person in People:
		if "Healer" in person.classTypes:
			compatible.append(person)

	return compatible

def getAllTanks(People):
	'''
	list of People -> list of People

	Takes the entire list of people, filter by if they are a tank
	'''
	compatible = []
	for person in People:
		if "Tank" in person.classTypes:
			compatible.append(person)
			
	return compatible

def getAllDPS(People):
	'''
	list of People -> list of People

	Takes the entire list of people, filter by if they are a DPS
	'''
	compatible = []
	for person in People:
		if "DPS" in person.classTypes:
			compatible.append(person)
			
	return compatible


def findHealers(day, time, People):
	'''
	int, int, list of Person -> list of Person

	Returns all combinations (specifically a tuple of 2) of healers that agree on the day and time currently being assessed.
	'''
	compatible = []
	for i in People:
		if time in i.availableTimes[day]:
			compatible.append(i)

	if len(compatible) < 2:
		return None

	ans = []
	for i in combinations(compatible, 2):
		ans.append(i)
	# print(ans)
	return ans


def findTanks(day, time, People):
	'''
	int, int, list of Person -> list of Person

	Returns all combinations of Tanks that agree on the day and time currently being assessed.
	'''
	compatible = []
	for i in People:
		if time in i.availableTimes[day]:
			compatible.append(i)
	if len(compatible) < 2:
		return None

	ans = []
	for i in combinations(compatible, 2):
		ans.append(i)
	return ans

def findDPS(day, time, People):
	'''
	int, int, list of Person -> list of Person

	Returns all combinations of DPS that agree on the day and time currently being assessed.
	'''
	compatible = []
	for i in People:
		if time in i.availableTimes[day]:
			compatible.append(i)
	if len(compatible) < 4:
		return None

	ans = []
	for i in combinations(compatible, 4):
		ans.append(i)
	return ans

def createClassList(arrayAsString):
	'''
	str -> list of str

	Array as String takes input of types tring, and returns the class list as a list.
	'''
	return arrayAsString.split(" ")

def createIntList(arrayAsString):
	'''
	str -> list of int or 'X'

	Takes a string of numbers, or 'X'

	Converts to an array of numbers and 'X'
	'''
	k = (arrayAsString.split(" "))
	result = []
	# print(k)
	for i in k:
		try:
			result.append(int(i))
		except ValueError:
			result.append("X")

	# print(result)
	return result

def parseInput(fileName):
	'''
	str -> list of Person

	Parses the input from a given list of files to create a list of Person to return.
	'''
	#The array of people to return.
	People = []

	f = open(fileName, 'r')
	for mainInput in f:
		arr = mainInput.split(",") #arr[0] should be name, arr[1] is of type mainClass, arr[2] are roles, arr[3 .. 9] are days for Monday -> Sunday
		newPerson = Person(arr[0])
		classesArray = createClassList(arr[2])
		[newPerson.addClass(x) for x in classesArray]

		for i in range(7):
			intArr = createIntList(arr[i+3])
			for j in intArr:
				if j == 'X':
					break
				else:
					newPerson.addTime(i + 1,j)

		People.append(newPerson)
	return People


def main():

	People = parseInput("input.txt")

	# [print(i) for i in People]

	#Sort the people into buckets for healers/DPS/tanks
	Healers = []
	Tanks = []
	DPS = []
	for person in People:
		Healers = getAllHealers(People) #Note that if we choose someone in Healers, we can't choose them again in the other roles. To think about later.
		Tanks = getAllTanks(People)
		DPS = getAllDPS(People)
		# if "Healer" in person.classTypes:
		# 	Healers.append(person)
		
		# if "Tank" in person.classTypes:
		# 	Tanks.append(person)
		# if "DPS" in person.classTypes:
		# 	DPS.append(person)

	# Testing:
	finalAns = {}
	for i in range(7):
		k = i + 1
		for j in range(24):
			a = findHealers(k, j, Healers)
			if a is None:
				#Skip to the next iteration.
				continue
			for i in a:
				# Create a copy of tanks for deletion purposes.
				copyOfTanks = list(Tanks)

				# we iterate over the tanks list, deleting anything that appeared in healers.
				givenHealers = []
				for ii in i:
					if ii in copyOfTanks:
						copyOfTanks.remove(ii)
					# continue
					# print(ii.name)
					givenHealers.append(ii)
				# print("")


				#Grab pairs from tanks.
				b = findTanks(k, j, copyOfTanks)

				if b is None:
					#Skip to next iteration
					continue
				for ii in b:
					copyOfDPS = list(DPS)

					givenTanks = []
					for i4 in givenHealers:
						# print(i4.name)
						if i4 in copyOfDPS:
							copyOfDPS.remove(i4)
					for iii in ii:
						if iii in copyOfDPS:
							copyOfDPS.remove(iii)
						givenTanks.append(iii)

					c = findDPS(k, j, copyOfDPS)
					if c is None:
						continue
					for iii in c:
						answer = []
						# print(iii.name)
						for i4 in givenHealers:
							answer.append(i4)
							# print(i4.name)
						for i4 in givenTanks:
							answer.append(i4)
							# print(i4.name)
						for i4 in iii:
							answer.append(i4)
							# print(i4.name)

						if tuple(answer) not in finalAns.keys():#If the team hasn't been gen'd yet, we put it into the finalAns, pointing to a dictionary of int -> listof integers
							finalAns[tuple(answer)] = {1 : [], 2 : [], 3 : [], 4 : [], 5 : [], 6 : [], 7 : []}
							finalAns[tuple(answer)][k].append(j)
						else: #The team has been generated, we add it to the finalAns.
							finalAns[tuple(answer)][k].append(j)

						# print("Finished w/ DPS")
						# print("")
	for i in finalAns:
		print("(%(A1)s, %(A2)s, %(A3)s, %(A4)s, %(A5)s, %(A6)s, %(A7)s, %(A8)s)" %{"A1" : i[0].name, "A2": i[1].name, "A3": i[2].name, "A4" : i[3].name, 
																					"A5": i[4].name, "A6": i[5].name, "A7": i[6].name, "A8": i[7].name})
		for j in finalAns[i]:
			print("\t%(A)d : %(B)s" %{"A": j, "B" : finalAns[i][j]})

		print("")

	# The main loop to find out possible agreed schedules
	# for i in range(7):
	# 	for j in range(24):
	# 		findHealers(i + 1, j, Healers)
	# 		findTanks(i + 1, j,  Tanks)
	# 		findDPS(i + 1, j, DPS)


if __name__ == "__main__": main()