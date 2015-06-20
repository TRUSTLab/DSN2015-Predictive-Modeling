# author: Ulya Bayram
# contact: ulyabayram@gmail.com

from determineOPUP import underOverCalculator
import math
import reliabilityCheck as synd

qlist = [int(0), float(95), float(99), float(99.9)]

fo = open('OverUnder_predictionResults.txt', 'w')

for q in qlist:
	fileName = str('MM_predictions_q_' + str(math.fabs(q)) + '.txt')
	with open(fileName, 'r') as file_predictions:
		delta_actual = [float(line3.split()[3]) for line3 in file_predictions]
	with open(fileName, 'r') as file_predictions:
		delta_pred = [float(line4.split()[4]) for line4 in file_predictions]
	with open(fileName, 'r') as file_predictions:
		actual = [float(line1.split()[1]) for line1 in file_predictions]
	with open(fileName, 'r') as file_predictions:
		predicted = [float(line2.split()[2]) for line2 in file_predictions]
	
	underOverCalculator(delta_actual, delta_pred, q, fo)
	numofdisksRAID = 8
	filenametosavesynd_nums = str('reliabilityAnalysisSyndNums_numdisks_' + str(numofdisksRAID) +\
						'_q_' + str(math.fabs(q)) + '.txt')
	filenametosavesynd_nums2 = str('numSyndromes_' + str(numofdisksRAID) +\
						'_q_' + str(math.fabs(q)) + '.txt')
	synd.SyndromesAndReliabilityCheck(filenametosavesynd_nums, filenametosavesynd_nums2, actual, predicted, delta_actual, delta_pred, numofdisksRAID)
