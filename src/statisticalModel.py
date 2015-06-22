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
