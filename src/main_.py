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

# imported libraries and python files
# make sure you have "glob, math, time, os" python libraries
from time import time
from clusterMain import mainForClustering
from clusterMain import log2_data
import statAnalysis1
from determineOPUP import underOverCalculator
from statisticalModel import mainStatisticalPred
import glob
import math
from plotplots import *
import os
import dataAnalysis as da
import reliabilityCheck as synd

# use trainAmount% of the dataset as training, user defined parameter
trainAmount = 50 

# modify below based on the folder your dataset is in
dataset = 'data'
directory = "../" + dataset

# method = 1 clusters the training set using kmeans
# method = 2 clusters the training set using meanshift
method = 2

if method == 1:
	clusterstr = 'kmeans'
	# parameter param of kmeans is k, the number of clusters
	# it is a user defined variable
	param = 11
elif method == 2:
	clusterstr = 'meanshift'
	# parameter param of the meanshift is the window size
	# it is in log2 base disk usage in terms of "byte"
	param = 5 # param = 5 results 8 clusters for sys_s
else:
	# statistical method is the third method we use in DSN2015 paper
	# to compare with Markov Modeling results
	clusterstr = 'statistical'

# list of quartiles we experiment with
# q = 0 means no quartile is used, in this case
# cluster centers are used, more info is provided below
q = [float(0), float(95), float(99), float(99.9)]

# set to 1 if you want to see some plots
plotFlag = 0

filenamelist = []
userList = []
deltadataList = []
ttDataSetdeltalog2 = {}
ttDataSetdelta = {}
ttDataSetDisk = {}

# get the ist of the filenames within the directory
fileNameList = glob.glob(str(directory+'/*.dat')) 

t0 = time()

# bring all training data together for clustering
# get training from all the files
for i in range(len(fileNameList)):
	
	tmplis = []
	tmplisw = []

	currentUserName = fileNameList[i]
	# extract user id from the filename
	userstr = 'user'
	stringIndexuser = currentUserName.index(userstr)
	strindexdot = currentUserName.index('.dat')
	userID = currentUserName[stringIndexuser+len(userstr):strindexdot]

	strFName = currentUserName

	# 3rd column has difference between previous and current usage (delta)
	with open(strFName, 'r') as f1:
		tmplis = [float(line.split()[2]) for line in f1] # delta bytes
	# 5th column has total data usage amount in terms of bytes
	with open(strFName, 'r') as f1:	
		tmplisw = [float(line.split()[4]) for line in f1] # total usage bytes
	
	# given the trainings %, find the exact index (row) where training ends
	trainUntilIndex = int(round(float(len(tmplis)*float(float(trainAmount)/float(100)))))

	userList = userList + [int(userID)]*len(tmplis[:trainUntilIndex])
	deltadataList = deltadataList + tmplis[:trainUntilIndex] # take training data only

	# list of all the data usage, delta, log2 delta, and total usage are stored
	# at the following dictionaries, indexed with user id's
	ttDataSetDisk[int(userID)] = tmplisw[:] #[trainUntilIndex-1:]
	ttDataSetdelta[int(userID)] = tmplis[:] #[trainUntilIndex:]
	ttDataSetdeltalog2[int(userID)] = log2_data(tmplis) #[trainUntilIndex:]) # save the test data for further use in log2

	#plotUserUsage(userID, log2_data(tmplis), dataset, trainUntilIndex)

t1 = time()
print "Time it takes to read all the usage dataset, divide to test and training: " + str(t1-t0)
#systemUsage = []	 
#systemUsage = da.findSystemDeltas(ttDataSetDisk, len(tmplis))
#plotContributionBars(systemUsage, ttDataSetdelta, dataset, trainUntilIndex)
#os.system('cd plots/sys_r/deltaChange/; gnuplot *.gp')

######## Clustering ##########
# do not perform clustering with the chosen parameter if it already exists, checked by if else
if method == 2: # meanshift
	foldernametosavestuff = str('results/'+ dataset + '/' + clusterstr + str(param))
	str_filename_set = []

	if not(os.path.exists(foldernametosavestuff)):
		t0 = time()
		centroids, clusterSeparatedHash, clusterList = mainForClustering(method, param, userList, deltadataList, foldernametosavestuff)
		if plotFlag == 1:
			plotClusters(str(clusterstr + str(param)))
		t1 = time()
		#print "Time it takes to cluster all the training data: " + str(t1-t0)
	# note that reading floats from file can cause slight error since they read files as binary data and make conversion
	# one difference is as; the real calculation and txt file had 1.76, but it is read as 1.75999999999
	
	else:
		# open and gather the saved clustering results
		t0 = time()
		with open(foldernametosavestuff + '/meanshiftCenters.txt', 'r') as fo:
			centroids = [float(line.split()[0]) for line in fo]
	
		with open(str(foldernametosavestuff + '/clusterList.txt'), 'r') as fo:
			clusterList = [int(line.split()[0]) for line in fo]

		fileNames = glob.glob(str(foldernametosavestuff + '/cluster_' + clusterstr + '*'))

		clusterSeparatedHash = {}
		for i in range(len(fileNames)): # for each cluster separated file, collect data
			users4HashList = []
			deltaHash2List = []
			#deltaHashList = []
			with open(fileNames[i], 'r') as file_clust:
				users4HashList = [int(line_1.split()[0]) for line_1 in file_clust]
			with open(fileNames[i], 'r') as file_clust: #log2
				deltaHash2List = [float(line_2.split()[2]) for line_2 in file_clust]
			#with open(fileNames[i], 'r') as file_clust: #bytes
			#	deltaHashList = [float(line_3.split()[1]) for line_3 in file_clust]

			currnameffile = str(fileNames[i])
			clusterNum = int(currnameffile[currnameffile.index(str('/cluster_' + clusterstr))+len(str('/cluster_' + clusterstr))])
			clusterSeparatedHash[clusterNum] = []
			clusterSeparatedHash[clusterNum].append(users4HashList)
			clusterSeparatedHash[clusterNum].append(deltaHash2List)
			#clusterSeparatedHash[clusterNum].append(deltaHashList)
			#print "ClusterSeparatedHash read from file for cluster number " + str(clusterNum)
			#print sum(clusterSeparatedHash[clusterNum][1])/float(len(clusterSeparatedHash[clusterNum][1]))
		
		t1 = time()
		#print "Time it takes to read all the clustering results, saved before: " + str(t1-t0)


	printModelsFlag = 0

	#crossvalidation(userList, clusterList, ttDataSetdeltalog2, centroids, trainUntilIndex)
	fres_overunderpredictionstuff = open(str(foldernametosavestuff + '/OverUnder_predictionResults.txt'), 'w')
	numofdisksRAID = 8

	for q_ in q:
		
		actual = []
		predicted = []
		delta_actual = []
		delta_pred = []

		stringMMpredictionfile = str(foldernametosavestuff+'/MM_predictions_q_' + str(math.fabs(q_)) + '.txt')
		# takes too much time to train MMs and perform predictions
		# if the file exists, skip overwriting it
		if not(os.path.exists(stringMMpredictionfile)):
			actual, predicted, delta_actual, delta_pred = statAnalysis1.statAnalyze(trainUntilIndex,
									foldernametosavestuff, clusterList, userList, q_, 
									ttDataSetdeltalog2, ttDataSetdelta, ttDataSetDisk, centroids, 
									clusterSeparatedHash, stringMMpredictionfile, printModelsFlag)
		else:
			with open(stringMMpredictionfile, 'r') as file_predictions:
				actual = [float(line1.split()[1]) for line1 in file_predictions]
			with open(stringMMpredictionfile, 'r') as file_predictions:
				predicted = [float(line2.split()[2]) for line2 in file_predictions]
			with open(stringMMpredictionfile, 'r') as file_predictions:
				delta_actual = [float(line3.split()[3]) for line3 in file_predictions]
			with open(stringMMpredictionfile, 'r') as file_predictions:
				delta_pred = [float(line4.split()[4]) for line4 in file_predictions]

		# take prediction results, perform analysis, find statistical occurrences of 
		# over and under predictions
		underOverCalculator(delta_actual, delta_pred, q_, fres_overunderpredictionstuff)
		filenametosavesynd_nums = str(foldernametosavestuff+'/reliabilityAnalysisSyndNums_numdisks_' + str(numofdisksRAID) +\
						'_q_' + str(math.fabs(q_)) + '.txt')
		filenametosavesynd_nums2 = str(foldernametosavestuff+'/numSyndromes_' + str(numofdisksRAID) +\
						'_q_' + str(math.fabs(q_)) + '.txt')
		synd.SyndromesAndReliabilityCheck(filenametosavesynd_nums, filenametosavesynd_nums2, actual, predicted, delta_actual, delta_pred, numofdisksRAID)

elif method == 1: # if kmeans is selected, repeat clustering nrepeat times, final result will be the average
	# user defined, feel free to change
	nrepeat = 30
	for nrep in range(nrepeat):
		foldernametosavestuff = str('results/'+ dataset + '/' + clusterstr + str(param) + '_' + str(nrep))
		str_filename_set = []

		if not(os.path.exists(foldernametosavestuff)):
			t0 = time()
			deltadataListcopy = copy.deepcopy(deltadataList)
			userListcopy = copy.deepcopy(userList)
			centroids, clusterSeparatedHash, clusterList = mainForClustering(method, param,
									userListcopy, deltadataListcopy, foldernametosavestuff)
			if plotFlag == 1:
				plotClusters(str(clusterstr + str(param) + '_' + str(nrep)))
			t1 = time()
			#print "Time it takes to cluster all the training data: " + str(t1-t0)
		# note that reading floats from file can cause slight error since they read files as binary data and make conversion
		# one difference is as; the real calculation and txt file had 1.76, but it is read as 1.75999999999
		
		else:
			t0 = time()
			with open(foldernametosavestuff + '/kmeansCenters.txt', 'r') as fo:
				centroids = [float(line.split()[0]) for line in fo]
	
			with open(str(foldernametosavestuff + '/clusterList.txt'), 'r') as fo:
				clusterList = [int(line.split()[0]) for line in fo]

			fileNames = glob.glob(str(foldernametosavestuff + '/cluster_' + clusterstr + '*'))

			clusterSeparatedHash = {}
			for i in range(len(fileNames)): # for each cluster separated file, collect data
				users4HashList = []
				deltaHash2List = []
				#deltaHashList = []
				with open(fileNames[i], 'r') as file_clust:
					users4HashList = [int(line_1.split()[0]) for line_1 in file_clust]
				with open(fileNames[i], 'r') as file_clust: #log2
					deltaHash2List = [float(line_2.split()[2]) for line_2 in file_clust]
				#with open(fileNames[i], 'r') as file_clust: #bytes
				#	deltaHashList = [float(line_3.split()[1]) for line_3 in file_clust]

				currnameffile = str(fileNames[i])
				clusterNum = int(currnameffile[currnameffile.index(str('/cluster_' + clusterstr))+\
						len(str('/cluster_' + clusterstr))])
				clusterSeparatedHash[clusterNum] = []
				clusterSeparatedHash[clusterNum].append(users4HashList)
				clusterSeparatedHash[clusterNum].append(deltaHash2List)
				#clusterSeparatedHash[clusterNum].append(deltaHashList)
				#print "ClusterSeparatedHash read from file for cluster number " + str(clusterNum)
				#print sum(clusterSeparatedHash[clusterNum][1])/float(len(clusterSeparatedHash[clusterNum][1]))
		
			t1 = time()
			#print "Time it takes to read all the clustering results, saved before: " + str(t1-t0)

		printModelsFlag = 0

		#crossvalidation(userList, clusterList, ttDataSetdeltalog2, centroids, trainUntilIndex)
		numofdisksRAID = 8

		for q_ in q:
			
			actual = []
			predicted = []
			delta_actual = []
			delta_pred = []

			stringMMpredictionfile = str(foldernametosavestuff+'/MM_predictions_q_' + str(math.fabs(q_)) + '.txt')
			# takes too much time to train MMs and perform predictions
			# if the file exists, skip overwriting it
			if not(os.path.exists(stringMMpredictionfile)):
				clusterListcopy = copy.deepcopy(clusterList)
				userListcopy = copy.deepcopy(userList)
				ttDataSetdeltalog2copy = copy.deepcopy(ttDataSetdeltalog2)
				ttDataSetdeltacopy = copy.deepcopy(ttDataSetdelta)
				ttDataSetDiskcopy = copy.deepcopy(ttDataSetDisk)
				centroidscopy = copy.deepcopy(centroids)
				clusterSeparatedHashcopy = copy.deepcopy(clusterSeparatedHash)

				actual, predicted, delta_actual, delta_pred = statAnalysis1.statAnalyze(trainUntilIndex,
										foldernametosavestuff, clusterListcopy, userListcopy, q_, 
										ttDataSetdeltalog2copy, ttDataSetdeltacopy,
										ttDataSetDiskcopy, centroidscopy, 
										clusterSeparatedHashcopy, stringMMpredictionfile, printModelsFlag)
			
else: # statistical analysis
	folder = str('results/' + dataset + '/' + 'statistical')

	if not(os.path.exists( folder )):
		os.mkdir(folder)

	ffile = open(str( folder +'/stat_overunderPValues.txt'), 'w')
	#filenamelist.append(str(folder+'/stat_overunderPValues.txt'))
	#titleset.append(folder)
	numofdisksRAID = 8

	for q_ in q:
		mainStatisticalPred(folder, trainUntilIndex, ttDataSetdelta, ttDataSetDisk, q_)
		
		stringMMpredictionfile = str(folder + '/statisticalPredictions' + str(q_) + '.txt')

		with open(stringMMpredictionfile, 'r') as file_predictions:
			actual = [float(line1.split()[1]) for line1 in file_predictions]
		with open(stringMMpredictionfile, 'r') as file_predictions:
			predicted = [float(line2.split()[2]) for line2 in file_predictions]
		with open(stringMMpredictionfile, 'r') as file_predictions:
			delta_actual = [float(line3.split()[3]) for line3 in file_predictions]
		with open(stringMMpredictionfile, 'r') as file_predictions:
			delta_pred = [float(line4.split()[4]) for line4 in file_predictions]

		underOverCalculator(delta_actual, delta_pred, q_, ffile)
		filenametosavesynd_nums = str(folder +'/reliabilityAnalysisSyndNums_numdisks_' + str(numofdisksRAID) +\
						'_q_' + str(math.fabs(q_)) + '.txt')
		filenametosavesynd_nums2 = str(folder +'/numSyndromes_' + str(numofdisksRAID) +\
						'_q_' + str(math.fabs(q_)) + '.txt')
		synd.SyndromesAndReliabilityCheck(filenametosavesynd_nums, filenametosavesynd_nums2, actual, predicted, delta_actual, delta_pred, numofdisksRAID)
		
