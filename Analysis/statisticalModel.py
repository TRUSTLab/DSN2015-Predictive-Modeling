# author: Ulya Bayram
# contact: ulyabayram@gmail.com

import os

def mainStatisticalPred(folder, trainUntilIndex, deltabyteLists, holdDiskUsage, q):


	fo = open(str(folder + '/statisticalPredictions' + str(q) + '.txt'), 'w')
	userList = deltabyteLists.keys()

# testing stage #################################
	for t in range(trainUntilIndex, len(deltabyteLists[int(userList[0])])): # for each new test data stored
		# for each user
		dpred = 0
		orig = []		
		dreal = 0
		preorig = 0
		
		for currUserNo in userList:
			preorig += holdDiskUsage[currUserNo][t-1]
	
			orig.append(holdDiskUsage[currUserNo][t])

			if q == 0:
				# first prediction for test data	
				dpred += sum(deltabyteLists[currUserNo][:t])/float(len(deltabyteLists[currUserNo][:t]))
								
			else:
				index4Quartile = int(round(len(deltabyteLists[currUserNo][:t])*float(float(q)/float(100))))
				if index4Quartile >= len(deltabyteLists[currUserNo][:t]):
					index4Quartile = len(deltabyteLists[currUserNo][:t])-1
				# do sorting
				if sum(deltabyteLists[currUserNo][:t]) != 0: # sort from min to max
					sortedList = sorted(deltabyteLists[currUserNo][:t])
					x_centersbytes = sortedList[index4Quartile]

				else: # = 0, simply give 0
					x_centersbytes = 0

				dpred += x_centersbytes

			dreal += deltabyteLists[currUserNo][t]

		print >> fo, (t-trainUntilIndex), sum(orig), (preorig+dpred), dreal, dpred

	
	return 
