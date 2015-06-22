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

# This python file performs 2  clustering methods: kmeans and a self-defined, simple, 1D version of meanshift

# make sure to have following imported python libraries
import random
import math
import os
import re
import shutil
from numpy  import array
import numpy as np
from copy import deepcopy
import time

########################################## Data Processing ########################################

# converts whole list into log2 base
def log2_data(data):
	result = []
	for i in range(len(data)):
		if data[i] > 0:
			result.append(math.log(data[i], 2))
		elif data[i] == 0:
			result.append(0)
		elif data[i] < 0:
			result.append(-1*math.log(-1*data[i], 2))
		else:
			print "ERROR: input usage data is not well defined!"
	return result

# converts a single data to log2 base
def log2singledata(data):
	if data > 0.0:
		result = math.log(data, 2)
	elif data == 0.0:
		result = 0.0
	elif data < 0.0:
		result = -1*math.log(-1*data, 2)
	else:
		print "ERROR: input usage data is not well defined!"
	return result

########################################### k-means clustering ###################################################
# Euclidean Distance
def Euclidean_Dist_1D(curr, center):
	dist = math.fabs(curr-center)
	return dist

# input is log2 base delta of disk usage in bytes
# and k the number of clusters
def kmeans_1D(data, k):
	
	# randomly distributed initial cluster centers
	initial_clust_centers = random.sample(np.linspace(min(data), 0, num = 100).tolist(), (k-1)/2)
	initial_clust_centers.extend([0])	
	initial_clust_centers.extend(random.sample(np.linspace(1, max(data)+1, num = 100).tolist(), (k-1)/2))
		
	currCenters = initial_clust_centers[:]
	
	# initial entropy
	entropy = 1000
	
	clusterBasedDataHolder = []
	counter = 0

	while entropy > 0.04: # iterations
		clusterList = []
		for d in range(k): # initialize to 0
			clusterBasedDataHolder.append([0, 0]) #first value for sum, second for length

		for i in range(len(data)):
			currentPoint = data[i] # take current data
			curr_dist = []

			# for each cluster center, find distances btw point and clust centers
			for j in range(len(currCenters)): 		
				curr_dist.append(Euclidean_Dist_1D(currentPoint, currCenters[j]))
		
			# assign it to closest center
			closestCent = curr_dist.index(min(curr_dist))	
			clusterBasedDataHolder[closestCent][0] += currentPoint
			clusterBasedDataHolder[closestCent][1] += 1
			clusterList.append(closestCent)

		preCenters = currCenters[:]

		tmpentro = 0
		for cc in range(len(currCenters)): # calculate new centers
			# there might be empty clusters
			if clusterBasedDataHolder[cc][1] != 0:
				# assign average as new cluster center
				currCenters[cc] = clusterBasedDataHolder[cc][0]/float(clusterBasedDataHolder[cc][1]) 
			else:
				currCenters[cc] = preCenters[cc]

			tmpentro += math.fabs(currCenters[cc]-preCenters[cc])
		entropy = tmpentro
		
	return clusterList, currCenters, clusterBasedDataHolder

# cluster based separation of the result, necessary for analysis
# so we can see text files of data points, one for each cluster
def separateClusters(cluster, clusterList, dataList, userList):
	newDataList = []
	newUserList = []
	
	for i in range(len(clusterList)):
		if clusterList[i] == (cluster):
			newDataList.append(dataList[i])
			newUserList.append(userList[i])
	
	return newDataList, newUserList 

################# Meanshift (or Sequential) Clustering, depends on the point of view ######################

def getMSClusters(datalog2, h):
	
	numclusters = 0
	clusterCentroids = []
	dataKeeperForMeanCalc = []

	for i in range(len(datalog2)): # for each training log2 delta data (they are ordered)
		closestCent = 0
		currPoint = datalog2[i]
		cnt = 0
		l_dist = []
		l_cluster = []
		
		for j in range(numclusters):
			# for each determined cluster center, if any
			# find the distance to centroid, sign matters
			distToCentroid = math.fabs(currPoint - clusterCentroids[j]) 
			
			# if distance is smaller than window defined, data might belong to that cluster
			if distToCentroid < h:
				# keep the distance of that point to current centroid 
				l_dist.append(distToCentroid) 
				# add that cluster id to list (cluster numbers are started from 1)
				l_cluster.append(j+1) 
				cnt = cnt + 1
		if cnt > 0: # if data point is found to be close to a centroid
			# get the id of the closest cluster
			closestCent = l_cluster[l_dist.index(min(l_dist))] 
			dataKeeperForMeanCalc[closestCent-1][0] = dataKeeperForMeanCalc[closestCent-1][0] + currPoint
			dataKeeperForMeanCalc[closestCent-1][1] = dataKeeperForMeanCalc[closestCent-1][1] + 1

			# first entry in list is sum of all data points, second entry is the number of data within cluster

		if closestCent > 0:
			clusterCentroids[closestCent-1] = dataKeeperForMeanCalc[closestCent-1][0]/float(dataKeeperForMeanCalc[closestCent-1][1])
                else: # initially, make the point the new cluster center            
                        clusterCentroids.append(currPoint)
			# keep the point, and the number of data in the cluster
			dataKeeperForMeanCalc.append([currPoint, 1]) 
			numclusters = numclusters + 1
		    
		tmpCenters = clusterCentroids[:]
		# continue until no more merges are possible
		while(len(tmpCenters)>2): 	
			currCenterVal = tmpCenters.pop(0)
			for t in range(len(tmpCenters)):
				currCenterVal2 = tmpCenters[t]
				tmpval = math.fabs(currCenterVal-currCenterVal2)
				if tmpval < h and (currCenterVal*currCenterVal2) >= 0:
					# merge these two clusters, update pointsToClust					
					indextobechanged = clusterCentroids.index(currCenterVal2)
					indextomerge = clusterCentroids.index(currCenterVal)					
					# update clustercentroids
					clusterCentroids[indextomerge] = (dataKeeperForMeanCalc[indextomerge][0]+\
						dataKeeperForMeanCalc[indextobechanged][0])/float(dataKeeperForMeanCalc[indextomerge][1]+\
						dataKeeperForMeanCalc[indextobechanged][1])
					del clusterCentroids[indextobechanged]
					dataKeeperForMeanCalc[indextomerge][0] = dataKeeperForMeanCalc[indextomerge][0] +\
						dataKeeperForMeanCalc[indextobechanged][0]
					dataKeeperForMeanCalc[indextomerge][1] = dataKeeperForMeanCalc[indextomerge][1] +\
						dataKeeperForMeanCalc[indextobechanged][1]
					del dataKeeperForMeanCalc[indextobechanged]
					

		numclusters = len(clusterCentroids)

	return clusterCentroids, dataKeeperForMeanCalc

def meanShift(datalog2, h):
	
	clusters, dataKeeperForMeanCalc = getMSClusters(datalog2, h)
	return clusters, dataKeeperForMeanCalc

# assigns all training data to the closest centroids found earlier
def findClosestMS4TrainingSet(centroids, data, userList, h, path_ms):
	# mean shift
	
	if os.path.exists(path_ms):
		shutil.rmtree(path_ms)
	os.mkdir(path_ms)

	f_o = []
	data2 = log2_data(data)
	clusterSeparatedHash = {}

	#create empty cluster files
	for nclust in range(len(centroids)):
		strName = 'cluster_meanshift' + str(nclust) + '.txt'
		f_o.append(open(os.path.join(path_ms, strName), 'w'))
		clusterSeparatedHash[nclust] = []	    	
		clusterSeparatedHash[nclust].append([])
		clusterSeparatedHash[nclust].append([])
		#clusterSeparatedHash[nclust].append([])
			
	clusters = []
	fo_clusterList = open(str(path_ms + '/clusterList.txt'), 'w')
	for i in range(len(data)):
		dist = []
		for nclust in range(len(centroids)):
			dist.append(math.fabs(centroids[nclust]-data2[i]))
		fclust = dist.index(min(dist))
		print >> f_o[fclust], userList[i], data[i], data2[i]
		clusters.append(fclust)
		clusterSeparatedHash[fclust][0].append(userList[i])
		clusterSeparatedHash[fclust][1].append(data2[i])
		#clusterSeparatedHash[fclust][2].append(data[i])
		# save clusterList to file
		print >> fo_clusterList, fclust

	return clusterSeparatedHash, clusters

# update the cluster centers, based on the final cluster assignment of outlier points
def meanshiftCentroids(clusterSeparatedHash):
	centroids = [0.0]*len(clusterSeparatedHash)

	for c in list(set(clusterSeparatedHash.keys())):
		centroids[c] = sum(clusterSeparatedHash[c][1])/float(len(clusterSeparatedHash[c][1]))

	return centroids

def findClosestCenter(centroids, currTestDatalog2):
	# takes, new test data, finds the closest cluster
	dist = []
	for nclust in range(len(centroids)):
		dist.append(math.fabs(centroids[nclust]-currTestDatalog2))
	fclust = dist.index(min(dist))
	#print >> f_o[fclust], userList[i], data[i], data2[i]
	return fclust

############################################### Main #############################################
def mainForClustering(clusterMethodChoice, param, userList, deltadataList, datasetsavefolderstr):
	# this is the main function
	# takes the text files, make differentiations	
		
	finaltraincentroids = []
	clusterSeparatedHash = {} # holds userNo's, log2deltas

	# apply kmeans on overall result
	if int(clusterMethodChoice) == 1: # kmeans
		# before kmeans, take log2 domain, keep the signs
		k = param
		
		clusters, kmcenters, dataKeeperForMeanCalc = kmeans_1D(log2_data(deltadataList), int(k))
		
		# check for empty clusters, if at least one empty cluster exists, to kmeans again
		check = True

		while check == True:
			counter = 0
			for iix in range(int(k)):
				if  dataKeeperForMeanCalc[iix][1] == 0:
					check = True # do the loop again
					break
				else:
					counter += 1

			if counter == int(k):
				check = False
				break		
			clusters, kmcenters, dataKeeperForMeanCalc = kmeans_1D(log2_data(deltadataList), int(k))
			
		path_km = datasetsavefolderstr # a new folder for each random km

		if os.path.exists(path_km):
			shutil.rmtree(path_km) # to remove it, make sure it exists
		os.mkdir(path_km)

		# create a different txt file for each cluster
		for i in range(int(k)):
			newdeltaDataList, newUserList = separateClusters(i, clusters, log2_data(deltadataList), userList)

			strName = 'cluster_kmeans' + str(i) + '.txt'
			with open(os.path.join(path_km, strName), 'w') as f_o:
		    		for fo1, fo2 in zip(newUserList, newdeltaDataList):
					print >> f_o, fo1, fo2

			# holds userNo's, log2deltas
			clusterSeparatedHash[i] = []
			clusterSeparatedHash[i].append(newUserList)
			clusterSeparatedHash[i].append(newdeltaDataList)

		finaltraincentroids = kmcenters[:]

	
	elif int(clusterMethodChoice) == 2: # meanshift

		h = param

		centroids, dataKeeperForMeanCalc = meanShift(log2_data(deltadataList), h)
		clusterSeparatedHash, clusters = findClosestMS4TrainingSet(centroids, deltadataList, userList, h, datasetsavefolderstr)
		finaltraincentroids = meanshiftCentroids(clusterSeparatedHash)

		with open(datasetsavefolderstr+'/meanshiftCenters.txt', 'w') as fo:
		    for i in range(len(finaltraincentroids)):
			fo1 = finaltraincentroids[i]
			print >> fo, fo1

	else:
		raise Exception("something wrong!")

	return finaltraincentroids, clusterSeparatedHash, clusters

