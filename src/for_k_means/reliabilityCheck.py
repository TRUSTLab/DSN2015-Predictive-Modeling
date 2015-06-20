import os
import math
import collections

def _counts(data):
    # Generate a table of sorted (value, frequency) pairs.
	table = collections.Counter(iter(data)).most_common()
	if not table:
		return table
    # Extract the values with the highest frequency.
	maxfreq = table[0][1]
	for i in range(1, len(table)):
		if table[i][1] != maxfreq:
			table = table[:i]
			break
	return table

def findMode(data):

	table = _counts(data)
	if len(table) == 1:
		return table[0][0]
	elif table:
		print "Error in Mode Calculation: no unique mode"
	else:
		print "Error in Mode Calculation"

def findMedian(data):

	data = sorted(data)
	n = len(data)
	if n == 0:
		print "Error in Median Calculation"
	if n%2 == 1:
		return data[n//2]
	else:
		i = n//2
	return (data[i - 1] + data[i])/2

# until here is taken from http://hg.python.org/cpython/file/3.4/Lib/statistics.py and changed a little
 
# inputs:
#	actual 		: original test set disk usage list
#	pred 		: predicted test set disk usage list
#	actualdelta	: original delta disk usage list
#	predelta	: predicted delta disk usage list
def SyndromesAndReliabilityCheck(filenametosave, filenametosave2, actual, pred, actualdelta, predelta, numd):
	fo = open(filenametosave, 'w')
	f2 = open(filenametosave2, 'w')
	dmax = max(actual) + max(actual)*float(0.1) # max amount of disk usage in the system

	bt = []
	improvement = []
	#numd = int(8)
	tofindmean = []
	#fcheck = open(filenametosave[:-4] + '_dr_check.txt', 'w')

	#averageimp = 0
	for t in range(len(actual)):
		
		dr = (dmax - pred[t])

		if pred[t] < actual[t]:
			dr = (dmax - actual[t])

		if pred[t] > dmax:
			dr = 0
		

		improvement = (20.4475 / (20.4475*(1-min([ (dr*numd/float(actual[t])), 1])) + (3.4069*min([dr*numd/float(actual[t]), 1]) )))
		y = (1-min([(dr*numd/float(actual[t])), 1]))

		bt.append(actual[t]/float(4096)) # 4 kb
		if t==0:
			dr_rel = 0 # initialization
		else:
			dr_rel = (dr/float(4096))/(float(bt[t-1]/float(numd)))

		#if dr*numd > actual[t]:
		#	print >> fcheck, t, (dr*numd-actual[t])
		tofindmean.append(dr_rel)
		print >> fo, improvement, dr, dmax, actual[t], pred[t], y, dr_rel
		print >> f2, dr_rel
		#averageimp += improvement

	#print str(filenametosave[:-4] + " --> " + str(averageimp/float(len(actual))))
	print  str(filenametosave[:-4] + " mean syndrome numbers --> " + str(sum(tofindmean)/float(len(tofindmean))))
	#print  str(filenametosave[:-4] + " mode --> " + str(findMode(tofindmean)))
	#print  str(filenametosave[:-4] + " median --> " + str(findMedian(tofindmean)))

def main_code():
	# main
	qlist = [int(-1), float(95), float(99), float(99.9)]

	k = [7, 9, 11]

	h = range(1, 11) #[2, 4, 8]
	fplot = open('plotReliabilitydelete.gp', 'w')

	# add statistical here
	for clusterMethodChoice in range(1, 3): # 1=km, 2=meanshift
		overunderrates = []
		#clusterMethodChoice = 1
		if clusterMethodChoice == 1: # kmeans
			print "Kmeans"
			for iik in range(len(k)):
				folder = str("kmeans/kmeans"+str(k[iik]))
				folder2 = str("kmeans"+str(k[iik]))
				print >> fplot, "set terminal postscript enhanced color\n"
				print >> fplot, "set ylabel \"Improvement\""
				print >> fplot, "set xlabel \"Time\""
				print >> fplot, "set grid x y"
				print >> fplot, "set key left top"
				print >> fplot, "set gri"
				print >> fplot, "set title \"Reliability Analysis " + folder + "\""
				print >> fplot, "set output \'| ps2pdf - Reliability_" + folder + ".pdf\'"
				print >> fplot, "plot",
				for q in qlist:
					tmpactual = []
					tmppred = []
					tmpactualdelta = []
					tmppreddelta = []
					filenametosave = "reliabili_" + folder2 + str(q) + ".txt"
				
					with open(str(folder+'/HMM_predictions_q_' + str(math.fabs(q)) + '.txt'), 'r') as fx:
						tmpactual = [float(line.split()[1]) for line in fx]
					with open(str(folder+'/HMM_predictions_q_' + str(math.fabs(q)) + '.txt'), 'r') as fx:
						tmppred = [float(line.split()[2]) for line in fx]
					with open(str(folder+'/HMM_predictions_q_' + str(math.fabs(q)) + '.txt'), 'r') as fx:
						tmpactualdelta = [float(line.split()[3]) for line in fx]
					with open(str(folder+'/HMM_predictions_q_' + str(math.fabs(q)) + '.txt'), 'r') as fx:
						tmppreddelta = [float(line.split()[4]) for line in fx]
					doReliabilityCheck(filenametosave, tmpactual, tmppred, tmpactualdelta, tmppreddelta)
					if q == qlist[len(qlist)-1]:
						print >> fplot, str("\"" + filenametosave + "\" using 0:1 with lines") #title " + "\"" + "q " + str(math.fabs(q)) + "\"")
					elif q == -1:
						print >> fplot, str("\"" + filenametosave + "\" using 0:1 with linestitle " + "\"" + "centroids" + "\","),
					else:
						print >> fplot, str("\"" + filenametosave + "\" using 0:1 with lines title " + "\"" + "q" + str(math.fabs(q)) + "\","),

		else: #meanshift
			print "MSSSSS"
			for iim in range(1, 11):
				folder = str("meanshift/meanshift"+str(iim))
				folder2 = str("meanshift"+str(iim))
				print >> fplot, "set terminal postscript enhanced color\n"
				print >> fplot, "set ylabel \"Improvement\""
				print >> fplot, "set xlabel \"Time\""
				print >> fplot, "set grid x y"
				print >> fplot, "set key left top"
				print >> fplot, "set gri"
				print >> fplot, "set title \"Reliability Analysis " + folder + "\""
				print >> fplot, "set output \'| ps2pdf - Reliability_" + folder + ".pdf\'"
				print >> fplot, "plot",

				for q in qlist:
					tmpactual = []
					tmppred = []
					tmpactualdelta = []
					tmppreddelta = []
					filenametosave = "reliabili_" + folder2 + str(q) + ".txt"
					with open(str(folder+'/HMM_predictions_q_' + str(math.fabs(q)) + '.txt'), 'r') as fx:
						tmpactual = [float(line.split()[1]) for line in fx]
					with open(str(folder+'/HMM_predictions_q_' + str(math.fabs(q)) + '.txt'), 'r') as fx:
						tmppred = [float(line.split()[2]) for line in fx]
					with open(str(folder+'/HMM_predictions_q_' + str(math.fabs(q)) + '.txt'), 'r') as fx:
						tmpactualdelta = [float(line.split()[3]) for line in fx]
					with open(str(folder+'/HMM_predictions_q_' + str(math.fabs(q)) + '.txt'), 'r') as fx:
						tmppreddelta = [float(line.split()[4]) for line in fx]	
					doReliabilityCheck(filenametosave, tmpactual, tmppred, tmpactualdelta, tmppreddelta)
					if q == qlist[len(qlist)-1]:
						print >> fplot, str("\"" + filenametosave + "\" using 0:1 with lines title " + "\"" + "q" + str(math.fabs(q)) + "\"")
					elif q == -1:
						print >> fplot, str("\"" + filenametosave + "\" using 0:1 with lines title " + "\"" + "centroids" + "\","),
					else:
						print >> fplot, str("\"" + filenametosave + "\" using 0:1 with lines title " + "\"" + "q" + str(math.fabs(q)) + "\","),

	folder = 'statistical'
	print >> fplot, "set terminal postscript enhanced color\n"
	print >> fplot, "set ylabel \"Improvement\""
	print >> fplot, "set xlabel \"Time\""
	print >> fplot, "set grid x y"
	print >> fplot, "set gri"
	print >> fplot, "set key left top"
	print >> fplot, "set title \"Reliability Analysis " + folder + "\""
	print >> fplot, "set output \'| ps2pdf - Reliability_" + folder + ".pdf\'"
	print >> fplot, "plot",
	for q in qlist:
		tmpactual = []
		tmppred = []
		tmpactualdelta = []
		tmppreddelta = []

		filenametosave = "reliabili_" + folder + str(q) + ".txt"

		with open(str(folder+'/statisticalPredictions' + str(q) + '.txt'), 'r') as fx:
			tmpactual = [float(line.split()[1]) for line in fx]
		with open(str(folder+'/statisticalPredictions' + str(q) + '.txt'), 'r') as fx:
			tmppred = [float(line.split()[2]) for line in fx]
		with open(str(folder+'/statisticalPredictions' + str(q) + '.txt'), 'r') as fx:
			tmpactualdelta = [float(line.split()[3]) for line in fx]
		with open(str(folder+'/statisticalPredictions' + str(q) + '.txt'), 'r') as fx:
			tmppreddelta = [float(line.split()[4]) for line in fx]
		doReliabilityCheck(filenametosave, tmpactual, tmppred, tmpactualdelta, tmppreddelta)

		if q == qlist[len(qlist)-1]:
			print >> fplot, str("\"" + filenametosave + "\" using 0:1 with lines title " + "\"" + str(math.fabs(q)) + "\"")
		elif q == -1:
			print >> fplot, str("\"" + filenametosave + "\" using 0:1 with lines title " + "\"" + "centroids" + "\","),
		else:
			print >> fplot, str("\"" + filenametosave + "\" using 0:1 with lines title " + "\"" + "q" + str(math.fabs(q)) + "\","),


	#os.system('gnuplot plotReliability.gp')
