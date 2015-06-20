Author: Ulya Bayram
Contact: ulyabayram@gmail.com

These codes are writen for a research project, published in DSN2015. If you use any of them, or if you use our dataset, please cite:

Ulya Bayram, Dwight Divine, Pin Zhou, Eric W. D. Rozier, "Improving reliability with dynamic syndrome allocation in intelligent software defined data centers", 45th Annual IEEE/IFIP International Conference on Dependable Systems and Networks (DSN), 2015.

How to run the codes:
=====================

To run the test, run main_.py file. By default, it is arranged to read sys_s dataset, we also provide this dataset in our repository. If you are using another dataset, then you should change the folder we read the dataset from, and columns we read. All the detailed information on which parameters to change and which parts to change are on comments within the codes.

Output of the tests are written to a folder named plots/sys_s. You should make sure you have both of these folders defined and exists within Analysis folder, otherwise you will get an error. You can change these default locations and structure, all you need to do is to follow the comments.

If you encounter problems, you can email me from the address I provide above.

main_.py is where we read the dataset and perform main operations, such as calling the function that clusters the training data, and calling the functions that creates MMs and perform predictions and then call the function that perform statistical analysis over the results such as computing over and under prediction rates. By following the comments, you can find out which function is which.

clusterMain.py is the file that contains clustering functions, k-means and a version of mean-shift that is more like a sequential clustering method.

MarkovModelsForUsers.py file has functions to create Markov Models and train them.

statAnalysis1.py is the file that has functions that create, train and test the Markov Models, calls functions in above file.

determineOPUP.py has function to determine over and under prediction rates.

reliabilityCheck.py computes the number of syndromes that can be fit to the space predicted as "not to be used".

Output files:
--------------

cluster_"method's name and cluster #".txt file has the data points and user id's that ended up inside the same cluster.

"clustering method"Centers.txt file has the centroids of the clusters determined after the clustering is complete.

MM_predictions_q_"quartile choice".txt has the prediction results, in given order: 
	row number, original disk usage in bytes, predicted disk usage in bytes, disk usage change wrt previous time step in bytes, predicted disk usage change in bytes

OverUnder_predictionResults.txt has over and under prediction rates, in the order:
	quartile choice, over prediction rate, under prediction rate, average over prediction, average under prediction, number of occurrences of under prediction, sum of under prediction amounts

numSyndromes_"# of disks"_q_"quartile choice".txt has the syndrome number that can be fit into the free space in that given time step, results we give our paper are averaged syndrome numbers, we print them on the screen as: 
	plots/sys_s/meanshift5/reliabilityAnalysisSyndNums_numdisks_8_q_99.9 mean syndrome numbers --> 2.95265867511

Important Note:
---------------

* Running mean-shift is easy, you run the code only once, it creates a folder with the name meanshift with the window parameter attached to it, you can find output files inside.

* Running k-means needs some attention, we run k-means with same parameter choice 30 times, you can change this repetition amount. Later, we run some codes to average the predictions, then perform over under predictions and syndrome number computations. You can find these codes within the folder "for_k_means". If you place the codes within this folder inside the main k-means folder that contains whole repetitions, you can get the outputs. Run average_kmeans.py to generate averaged predictions over k-means runs, then when you have MM_prediction....txt files created, run underoverforkmeans.py, no further operations required.

* Statistical perdiction code is inside statisticalModel.py. If you do not pick mean-shift with "method = 2" or k-means with "method = 1", then any other number would run this code from main_.py. Results will be inside "statistical" folder.
