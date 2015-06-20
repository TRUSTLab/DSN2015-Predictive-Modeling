# author: Ulya Bayram
# contact: ulyabayram@gmail.com

# statistical analysis, where MMs and and centroids are used
# for performing predictions over the data

import os
import copy
import math
import shutil
from MarkovModelsForUsers import createMM
from MarkovModelsForUsers import updateMM
from MarkovModelsForUsers import convertLog2DataToM
from clusterMain import log2_data
from clusterMain import log2singledata
from clusterMain import findClosestCenter
from plotplots import *
from time import time

# used to take the power of the matrix
# not used within the code any more
# can be useful for other researchers
def matrixPower(P, r):
	# inputs:
	# 	P: square matrix
	#	r: power
	if r <= 0:
		raise Exception("Matrix power cannot be zero or less!")
	elif r==1:
		return P
	else:		
		subP = []
		subP = copy.deepcopy(P)
		for repeat in range(r-1):
			newMatrix = []
			for i in range(len(P)):
				row = []
				row.append(P[i])
				tmpRow = []
				for j in range(len(P)):
					col = []					
					col.append([tmp[j] for tmp in subP])
					val = sum([row[0][t]*col[0][t] for t in range(len(P))])
					tmpRow.append(val)
				newMatrix.append(tmpRow)
			del subP
			subP = copy.deepcopy(newMatrix)
			
		return newMatrix

# Important part of predictions
# 
def p_i(i, t, userNo, P_trans):
	# inputs:
	#	i: initial state (given) (i of p_i)
	#	t: number of iterations (time)
	#	userNo: needed to retrieve MM transition matrix from txt file-starts from 0th user

	#p_i_0 = []
	p_i_res = []
	#calculate new p_i
	for j in range(len(P_trans)):
		if j == i:
			#p_i_0.append(float(1))
			p_i_res = P_trans[i][:]
			#print p_i_res
			return p_i_res		

# performs the prediction
# multiplication of the state occupancy probability vector by 
# delta bytes representing every state based on q selection
def calculateD(x_centers, p_i_res):	
	
	d = sum([x_centers[tt]*p_i_res[tt] for tt in range(len(x_centers))])		

	return d

# take inverse of log2, which is power of 2 to recover bytes of delta disk usage
def inv_log2(data_i):
	if float(data_i) > 0:
		return float(math.pow(2, float(data_i)))
	elif float(data_i) < 0:
		return -1*float(math.pow(2, -1*float(data_i)))
	elif float(data_i) == 0:
		return float(0)
	else:
		return 0

# converts the cluster centers that are in log2 base
# into bytes, 
# for the no quartile case, it simply uses cluster centers in bytes
# for quartile q != 0 case, it finds the index of qth quartile within the clusters
# and converts them into bytes,
# x_centerbytes is the returning result, a byte value from each cluster
def get_x_centers(clustercenters, q, clusterSeparatedHash):

	#x_centerslog2 = [] # in log2 domain
	x_centersbytes = []

	if q == float(0): # use mean centers of centroids	
		for cc in range(len(clustercenters)):
			x_centersbytes.append(inv_log2(clustercenters[cc]))

		#x_centerslog2 = clustercenters[:] #log2
	else: # use quartiles
		
		# take files and file inputs for each cluster from folder you created before
		#x_centerslog2 = [0]*len(clusterSeparatedHash)
		x_centersbytes = [0]*len(clusterSeparatedHash)

		# for each cluster
		for i in range(len(clusterSeparatedHash)):
			
			data2List = []
			data2List = clusterSeparatedHash[i][1][:] # log2 delta
			index4Quartile = int(round(len(data2List)*float(float(q)/float(100))))-1 
			# -1 is for python indexing, wouldn't matter much though

			if index4Quartile >= len(data2List):
				index4Quartile = len(data2List)-1 # take the last value (the max)

			# do sorting
			if sum(data2List) != 0: # sort from min to max
				sorted2List = sorted(data2List)
				#x_centerslog2[i] = sorted2List[index4Quartile]
				x_centersbytes[i] = inv_log2(sorted2List[index4Quartile])	
			else: # = 0, simply give 0
				#x_centerslog2[i] = 0
				x_centersbytes[i] = 0

	return x_centersbytes

# main part for test, this is where the predictions are performed
# trainUntilIndex = index that separates training data from test data
# folder = the folder to save the txt files containing user-based prediction results
# clusterList = result of clustering, complete set of training data, converted into cluster ids they belong to
# userList = the users list that is the owner of the data points above
# q = quartile selection
# ttDatasetHashdeltalog2 = A dictionary containing delta disk usage amounts of users in log2 base
# ttDatasetHashdelta =  A dictionary containing delta disk usage amounts of users in bytes
# ttDatasetHashdisk = A dictionary containing disk usage amounts of users in bytes
# centroids =  cluster centroids
# clusterSeparatedHash = A dictionary, contains data separated by cluster ids
# stringMMpredictionfile = string of file name to save the prediction results
# printModelsFlag = flag, 0 means no plots, 1 means plot the MM results
def statAnalyze(trainUntilIndex, folder, clusterList, userList, q, ttDatasetHashdeltalog2, 
		ttDatasetHashdelta, ttDatasetHashdisk, centroids, 
		clusterSeparatedHash, stringMMpredictionfile, printModelsFlag):

	# open the prediction file, make ready for writing
	fo_predictions = open(stringMMpredictionfile, 'w')
	# number of clusters obtained during training clustering stage previously
	k = len(centroids)
	
	start_hash = {}
	transMM_hash = {}
	rawMM_hash = {}

	# Step: create Markov Models for each user based on training clusters
	if printModelsFlag == 1:
		# Create MM folder or Write Over It If Exists
		path_mm = str(folder + "/" + 'MMs' + str(math.fabs(q)))
		if os.path.exists(path_mm):
			shutil.rmtree(path_mm)
		os.mkdir(path_mm)

	#ts0 = time()

	############## CREATING & TRAINING MARKOV MODELS STEP #######################################
	for currUser in list(set(userList)): # for each user
		# find first index list of the current user within merged clustering result
		startOfUser = userList.index(currUser)
		i = startOfUser
		currClusters = []
		
		# take the user's data in this while loop, find the symbol list of this user
		while((i < len(userList)) and (userList[i] == currUser)):
			currClusters.append(clusterList[i])				
			i = i + 1
		
		# create a Markov Model for the current user, using its training symbol list (clustering results)
		transMM, rawMM, startstate = createMM(k, currClusters)	
		start_hash[currUser] = startstate # not used anywhere
		# state transition probability matrix
		transMM_hash[currUser] = transMM[:]
		# transition counts matrix, without converting into probabilities
		rawMM_hash[currUser] = rawMM[:]

		if printModelsFlag == 1:
			plotMMs(transMM_hash[currUser], currUser, start_hash[currUser], 
				str(path_mm + "/res_trained_" + str(currUser) + "-MM.dot"), centroids)
			strTmp = "cd " + path_mm + ";" + "dot -Tpng res_trained_" + str(currUser) + \
				"-MM.dot -o " "res_trained_" + str(currUser) + "-MM.png"
			os.system(strTmp)

	################################# TRAINING END, One MM is created for every user  ###################

	#ts1 = time()
	#print "Time it takes to train all Markov Models of all users: " + str(ts1-ts0)
	
	# for predictions, get the byte delta's from each cluster (state)
	x_centersbyte = get_x_centers(centroids, q, clusterSeparatedHash) 

	# Part below is just for analysis when coding
	# fxcenters = open(str(folder+'/control_xcenters_' + str(math.fabs(q)) + '.txt'), 'w')
	# fx2centers = open(str(folder+'/control_xcenterssymbols_' + str(math.fabs(q)) + '.txt'), 'w')
	# print >> fxcenters, x_centersbyte
	################################ TESTING BEGINS - CALCULATE AND STORE d ################################
	
	storecentroids = centroids[:]
	# print storecentroids

	actual_disk = []
	pred_disk = []
	actual_delta = []
	pred_delta = []
	new_clusterSeparatedHash = {}
	new_clusterSeparatedHash = copy.deepcopy(clusterSeparatedHash)
	new_start_hash = {}
	new_start_hash = copy.deepcopy(start_hash)

	# treat every test data as an online observation
	# we predict using the previous MMs first, then observe the test data
	# store both results and compare later
	# before observing the next test data, we update clusters by including new observation
	# also we update MMs of each user by including new observation
	for testIndex in range(trainUntilIndex, len(ttDatasetHashdeltalog2[currUser])):
		d_sys_pred = 0
		dreal = 0
		dtmp = 0
		orig = []
		orig2 = []

		for currUserNo in list(set(userList)): # for each user					

			#  find state occupancy probability vector
			p_i_res = p_i(int(new_start_hash[currUserNo]), 1, currUserNo, transMM_hash[currUserNo])
			# find the predicted delta of disk usage of the current time step before we observe it
			dtmp = calculateD(x_centersbyte, p_i_res)
			# sum the predictions over all users, we're not concerned about user-based predictive performance
			d_sys_pred += dtmp
			
			# now on, do updates
			presymbol = int(new_start_hash[currUserNo])
			currsymbol = int(findClosestCenter(storecentroids, ttDatasetHashdeltalog2[currUserNo][testIndex]))
			#print >> fx2centers, "------ below -----"
			bytecentroidsconverted = []
			bytecentroidsconverted = [inv_log2(storecentroids[ssx]) for ssx in range(len(storecentroids))]
			#print >> fx2centers, centroids
			#print >> fx2centers, storecentroids
			#print >> fx2centers, "test data " + str(ttDatasetHashdeltalog2[currUserNo][testIndex])
			#print >> fx2centers, "user " + str(currUserNo) + " test data no " + str(testIndex)
			#print >> fx2centers, "prediction " + str(log2singledata(dtmp))
			#print >> fx2centers, "determined symbol " + str(currsymbol)
			#print >> fx2centers, "cluster mean training " + str(sum(clusterSeparatedHash[currsymbol][1])/float(len(clusterSeparatedHash[currsymbol][1])))
			
			# update the clusterSeparatedHash by adding the observed test data
			new_clusterSeparatedHash[currsymbol][0].append(currUserNo)
			new_clusterSeparatedHash[currsymbol][1].append(ttDatasetHashdeltalog2[currUserNo][testIndex])

			#print >> fx2centers, "cluster mean test included " + str(sum(new_clusterSeparatedHash[currsymbol][1])/float(len(new_clusterSeparatedHash[currsymbol][1])))
			#print >> fx2centers, "----end ------"
			
			# update cluster centers
			storecentroids[currsymbol] = sum(new_clusterSeparatedHash[currsymbol][1])/float(len(new_clusterSeparatedHash[currsymbol][1]))
			#print >> fxcenters, storecentroids, log2singledata(dtmp), sum(new_clusterSeparatedHash[currsymbol][1])/float(len(new_clusterSeparatedHash[currsymbol][1]))
			# set of centers in terms of bytes of difference, update x_centerbyte for the next step
			x_centersbyte = get_x_centers(storecentroids, q, new_clusterSeparatedHash)
			#print >> fxcenters, x_centersbyte
			# holdata has real deltas of that user in terms of bytes
			
			#if (printModelsFlag == 1) and (testIndex == (len(ttDatasetHashdeltalog2[currUser])-1)): # updated MM versions
			#	plotMMs(transMM_hash[currUserNo], currUserNo, start_hash[currUserNo], 
			#		str(path_mm + "/res_updated_" + str(currUserNo) + "-MM.dot"), centroids)
			#
			#	strTmp2 = "cd " + path_mm + ";" + "dot -Tpng res_updated_" + str(currUserNo) +\
			#		"-MM.dot -o " "res_updated_" + str(currUserNo) + "-MM.png"
			#	os.system(strTmp2)
					
			transMM_hash[currUserNo], rawMM_hash[currUserNo] = updateMM(rawMM_hash[currUserNo], currsymbol, presymbol)
			new_start_hash[currUserNo] = currsymbol
			
			orig.append(ttDatasetHashdisk[currUserNo][testIndex]) # current whole
			orig2.append(ttDatasetHashdisk[currUserNo][testIndex-1]) # previous whole
			dreal += ttDatasetHashdelta[currUserNo][testIndex] # real delta bytes

		# save to the file we opened at the beginning to save the predictions the following, for each time step
		# (testIndex-trainUntilIndex) = to show our indexing is correct
		# sum(orig) = overall disk usage in the system
		# sum(orig2)+d_sys_pred = overall predicted disk usage on the system
		# dreal = overall real delta of disk usage in the system
		# d_sys_pred = overall predicted delta of disk usage in the system
		print >> fo_predictions, (testIndex-trainUntilIndex), sum(orig), sum(orig2)+d_sys_pred, dreal, d_sys_pred
		actual_disk.append(sum(orig))
		pred_disk.append(sum(orig2)+d_sys_pred)
		actual_delta.append(dreal)
		pred_delta.append(d_sys_pred)
	##########################################################################################################

	#rewrite x_centers, all cluster centers have changed after all test data
	r_x_centers = [convertLog2DataToM(math.fabs(storecentroids[xu])) for xu in range(len(storecentroids))]
	#print >> fxcenters, r_x_centers
	#print >> fxcenters, storecentroids
	return actual_disk, pred_disk, actual_delta, pred_delta

