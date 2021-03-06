# author: Ulya Bayram
# contact: ulyabayram@gmail.com
#
# Copyright (c) 2015 Trustworthy Systems Laboratory at the University of Cincinnati 
# All rights reserved.
#
# Developed by: 		
#	  		Trustworthy Systems Laboratory
#                      	University of Cincinnati
#                        http://dataengineering.org
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal with the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimers.
#
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimers in the documentation and/or other materials provided with the distribution.
# Neither the names of the Trustworthy Systems Laboratory, the University of Cincinnati, nor the names of its contributors may be used to endorse or promote products derived from this Software without specific prior written permission.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE SOFTWARE.

import numpy
import os
import shutil
import math
import copy

# convert log2 base bytes into Megabytes
# for visualization of Markov Models
def convertLog2DataToM(data):
	# take log2data centroids (float) as input
	# return strings with K or M or G
	
	# data is never 0, and always >0
	bytes = math.pow(2, data)
	
	if bytes < 1024:
		return str('%5.3fB' % bytes)
	elif bytes < (1024*1024):
		bytes = float(bytes / 1024)
		return str('%5.3fK' % bytes)
	elif bytes < (1024*1024*1024):
		bytes = float(bytes / (1024*1024))
		return str('%5.3fM' % bytes)
	else:
		bytes = float(bytes / (1024*1024*1024))
		return str('%5.3fG' % bytes)

# takes each user data and clustering result
# creates MMs for each user
def createMM(numStates, currClusters):
	
	# transition matrix initialization
	transMM = numpy.zeros(shape = (numStates,numStates))
	rawMM = []
	
	preSymbol = -1
	
	for i in range(len(currClusters)):
		if preSymbol == -1: # means this is first cluster/state
			preSymbol = currClusters[i]
			#truestartState = preSymbol
		else:
			transMM[preSymbol, currClusters[i]] += 1
			preSymbol = currClusters[i]
			#startState = currClusters[i] # last one is the start state for first pi

	rawMM = copy.deepcopy(transMM)

	# create probabilities for transitions between states
	for i in range(numStates):
		denom = float(sum(transMM[i])) # sum of each row
		for j in range(numStates):
			if (denom > 0) and (transMM[i, j] != float(0)):
				transMM[i, j] = float(transMM[i, j]/denom)
			
	return transMM.tolist(), rawMM.tolist(), preSymbol


# take previous rawMM counter of this user
# update by current input cluster result
# divide by denom, return transMM probabilities
def updateMM(rawMM, inputcluster, precluster):
	rawMM[precluster][inputcluster] += 1
	p = numpy.zeros(shape = (len(rawMM),len(rawMM)))

	for i in range(len(rawMM)):
		denom = float(sum(rawMM[i])) # sum of each row

		for j in range(len(rawMM)):
			if denom > 0:
				p[i, j] = float(rawMM[i][j]/denom)

	return p.tolist(), rawMM

# used when building this code to test things,
# not used in anywhere of the code-set any more
def mainMM(clusteringChoice):
	# main
	# kmeans first
	userList = []
	clusterList = []
	dataList = []

	if clusteringChoice == 1: #kmeans
		fdata = open('kmeansClusters.txt', 'r')
	else: #meanshift
		fdata = open('meanshiftClusters.txt', 'r')

	for line in fdata:
		xtmp = 	line.split()
		userList.append(int(xtmp[0]))
		clusterList.append(int(xtmp[1]))
		dataList.append(float(xtmp[2]))

	k = max(clusterList)+1

	# MM folder
	path_MM = 'MMs'
	shutil.rmtree(path_MM)
	os.mkdir(path_MM)
	start_hash = {}

	for currUser in list(set(userList)): # for each user
		# find first index list of current user
		startOfUser = userList.index(currUser)
		i = startOfUser
		matchIndex = []
		currClusters = []
		currData = []

		# take the user's data in this while loop
		while((userList[i] == currUser) and (i < len(userList)-1)):
			currClusters.append(clusterList[i])
			currData.append(dataList[i])
			matchIndex.append(i)
			i = i + 1
	
		transMM, startstate = createMM(k, currUser, currClusters, clusteringChoice)
		start_hash[currUser] = startstate
		strname = str(currUser) + "-MM.txt"
		fMM = open(os.path.join(path_MM, strname), 'w')
		for xx in range(k):
			print >> fMM, transMM.tolist()[xx]

		strTmp = "cd MMs; dot -Tpng " + str(currUser) + "-MM.dot -o " + str(currUser) + "-MM.png"
		#print strTmp
		os.system(strTmp)
	

	return list(set(userList)), start_hash
