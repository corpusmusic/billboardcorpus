import numpy as np
import scipy as sp
import scipy.stats
import csv
from collections import defaultdict
import os
import time

def load_csv(filename):
	transDict = defaultdict(list)
	with open(filename,'rb') as f:
		reader = csv.reader(f, delimiter='\t', quotechar='"' )
		for row in reader:
			valuesList = row
			for index,value in enumerate(valuesList):
				transDict[index].append(value)
		return transDict

#look at zeros vs non zeros 
	
def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return [m, m-h, m+h]


#generate table

#assume that the format is I-I, I-bII I-II, I-bIII ... I-VII, II-I, II-bII ... VII-VII 

meanTable = []
intervalTable = []
meanTableNoZeros = []
intervalTableNoZeros = []

disDict = load_csv('outputFIXED2.txt')
for key in range(145):
	if key != 0:
		data = [float(x) for x in disDict[key][1:]]
		datanozeros = filter(lambda x: x != 0, data)
		con = mean_confidence_interval(data)
		conNoZeros = mean_confidence_interval(datanozeros)

		meanTable.append(round(con[0],4))
		meanTableNoZeros.append(round(conNoZeros[0],4))
		intervalTable.append(str(round(con[1],4)) + "-" + str(round(con[2],4)) )
		intervalTableNoZeros.append(str(round(conNoZeros[1],4)) + "-" + str(round(conNoZeros[2],4)) )
		
meanTable = [meanTable[i:i+12] for i in xrange(0,len(meanTable),12)]
meanTableNoZeros = [meanTableNoZeros[i:i+12] for i in xrange(0,len(meanTableNoZeros),12)]
intervalTable = [intervalTable[i:i+12] for i in xrange(0,len(intervalTable),12)]
intervalTableNoZeros = [intervalTableNoZeros[i:i+12] for i in xrange(0,len(intervalTableNoZeros),12)]
	
		

