# takes the prediction file as input: fileName
def underOverCalculator(real, pred, q, fres):

	opflag = 0
	upflag = 0
	sumOp = 0
	sumUp = 0

	# for each test data
	for i in range(len(pred)):
		if pred[i] >= real[i]: # if predicted delta is larger than original delta
			opflag += 1 # overprediction detected
			sumOp += (pred[i]-real[i]) # amount of overprediction
		else: # underprediction
			upflag += 1
			sumUp += (real[i]-pred[i]) # amount of underprediction
	

	opRate = opflag / float(len(pred)) # overprediction occurrence rate
	upRate = upflag / float(len(pred)) # underprediction occurrence rate
	
	avgOP = sumOp/ float(opflag) # average overprediction within whole test set (single value)

	if upflag > 0:
		avgUP = sumUp / float(upflag) # average underprediction within whole test set (single value)
	else:
		avgUP = 0

	# result = [float(q/float(100)), opRate, upRate, avgOP, avgUP, upflag, sumUp]
	 
	print >> fres, float(q/float(100)), opRate, upRate, avgOP, avgUP, upflag, sumUp
