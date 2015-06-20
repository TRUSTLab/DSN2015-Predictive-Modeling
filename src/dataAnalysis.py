# author Ulya Bayram
# ulyabayram@gmail.com
# input is the dictionary 
# each key is the uderID
# for each user, it contains the delta's w/d
def findSystemDeltas(userDeltaDict, lengthoftime):
	keylist = userDeltaDict.keys()
	
	systemsChange = []

	# initially create an empty systems list, all elements 0
	for t in range(lengthoftime):
		systemsChange.append(0)

	currListofDelta = []

	for x in keylist: # take current user ID key
		currListofDelta = userDeltaDict[x][:] # copy the values

		for t in range(lengthoftime):
			systemsChange[t] += currListofDelta[t]

	return systemsChange
