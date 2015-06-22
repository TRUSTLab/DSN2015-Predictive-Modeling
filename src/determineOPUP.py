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

# inputs are real and predicted overall results
# selected quartile % (or no quartile) to indicate which result is from which q
# and fres, the file to write the results on
def underOverCalculator(real, pred, q, fres):

	opflag = 0
	upflag = 0
	sumOp = 0
	sumUp = 0

	# for each test data
	for i in range(len(pred)):
		# if predicted delta is larger than original delta
		if pred[i] >= real[i]: 
			opflag += 1 # overprediction detected
			sumOp += (pred[i]-real[i]) # amount of overprediction
		else: # underprediction detected
			upflag += 1
			sumUp += (real[i]-pred[i]) # amount of underprediction
	

	opRate = opflag / float(len(pred)) # overprediction occurrence rate
	upRate = upflag / float(len(pred)) # underprediction occurrence rate

	# average overprediction within whole test set (single value)
	avgOP = sumOp/ float(opflag) 

	if upflag > 0:
		# average underprediction within whole test set (single value)
		avgUP = sumUp / float(upflag) 
	else:
		avgUP = 0

	# result = [float(q/float(100)), opRate, upRate, avgOP, avgUP, upflag, sumUp]
	 
	# write to the file fres opened in main_.py file the following
	# quartile %, over prediction rate, 
	# under prediction rate, 
	# average over prediction amount, average underprediction amount
	# how many times underprediction occurred
	# sum of underprediction amount
	print >> fres, float(q/float(100)), opRate, upRate, avgOP, avgUP, upflag, sumUp
