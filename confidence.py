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


def write_csv(table,name):
	with open(name, 'wb') as f:
		writer = csv.writer(f)
		rowNames = [[name,"I","bII","II","bIII","III","IV","bV","V","bVI","VI","bVII","VII"]]

		for index,row in enumerate(table):
			row.insert(0,rowNames[0][index+1]) 		

		writer.writerows(rowNames)
		writer.writerows(table)

#generate table

def generate_tables(chunk):
#assume that the format is I-I, I-bII I-II, I-bIII ... I-VII, II-I, II-bII ... VII-VII 

	meanTable = []
	intervalTable = []
	meanTableNoZeros = []
	intervalTableNoZeros = []

	disDict = load_csv('output4bars.csv')
	for key in range(145):
		if key != 0:
			data = [float(x) for x in disDict[key][1:]]
			data = data[chunk*730: (chunk+1)*730]	
	
			datanozeros = filter(lambda x: x != 0, data)
			
			print datanozeros

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

	write_csv(meanTable,"meanTransistionProbabilities" + str(chunk))
	write_csv(meanTableNoZeros, "MeanTransitionProbabilitiesNoZero" + str(chunk))
        write_csv(intervalTable, "ConfidenceIntervalTransitionalProbabilities" + str(chunk))
        write_csv(intervalTableNoZeros, "ConfidenceIntervalTransitionalProbabilitiesNoZero" + str(chunk))
	
		
generate_tables(0)
generate_tables(1)
generate_tables(2)
generate_tables(3)

