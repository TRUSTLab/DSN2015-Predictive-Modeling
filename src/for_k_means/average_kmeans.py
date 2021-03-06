# author: Ulya Bayram
# contact: ulyabayram@gmail.com

# this code is to average over all kmeans trials with same k
# and perform the same predictive analysis
import math

strfolder = 'kmeans11_'

q = [float(0), float(95), float(99), float(99.9)]


for q_ in q:
	avgPredsdisk = [0]*1069
	avgPredsdelta = [0]*1069
	origdisk = [0]*1069
	origdelta = [0]*1069

	for i in range(30):
		filename = strfolder + str(i) + '/MM_predictions_q_' + str(math.fabs(q_)) + '.txt'
		fo = open(filename, 'r')
		c = 0

		for line in fo:
			avgPredsdisk[c] += float(line.split()[2])
			avgPredsdelta[c] += float(line.split()[4])
			
			if i == 29:
				origdisk[c] = float(line.split()[1])
				origdelta[c] = float(line.split()[3])

			c += 1

	f2 = open(str('MM_predictions_q_' + str(math.fabs(q_)) + '.txt'), 'w')
	for l in range(1069):
		print >> f2, l, origdisk[l], avgPredsdisk[l]/30.0, origdelta[l], avgPredsdelta[l]/30.0
