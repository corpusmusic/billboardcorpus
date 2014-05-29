#clusterize.py

#HOW TO USE: This script uses arguments! Run with this command:
#	$ python clusterize.py file_with_cluster_data file_with_all_data prefix_of_output_files
#
#EXAMPLE: $ python clusterize.py output3_K_G8.kgg AlldataWithNonHarmonicsV5.csv cluster 
#
#This script will divide all data into different clusters.
#The CLUSTER_GROUP_FILE contains songs with corresponding cluster
#numbers. The script will parse the cluster group file 
#into lists that represents each cluster. All these cluster 
#lists are kept inside a dictionary, with a cluster_id number 
#as the key. Then, match each cluster list with data from
#the all data file, and create a csv file for each cluster.

import re, sys, csv

#Default arguments for script.
CLUSTER_GROUP_FILE = "output3_K_G8.kgg"
ALL_DATA_FILE = "AlldataWithNonHarmonics.csv"
OUTPUT_FILE_PREFIX = "cluster"

#Custom arguments.
if len(sys.argv) > 1: 
	CLUSTER_GROUP_FILE = sys.argv[1]
if len(sys.argv) > 2:
	ALL_DATA_FILE = sys.argv[2]
if len(sys.argv) > 3:
	OUTPUT_FILE_PREFIX = sys.argv[3]


def read_file(filename):
	with open(filename, "r") as file:		#Open file

		#read the file, split into lines.
		data = file.read()
		data = re.split(r'\n',data)
	
	return data

def build_clusters(data):
	#Regex to find cluster group numbers.
	cluster_regex = re.compile('\d+$')
	#Regex to find song names.
	song_regex = re.compile('\S+')
	#Dictionary storing cluster groups.
	clusters = {}

	#For each line in the data...
	for line in data:

		#Match for the cluster number.
		cluster_match = cluster_regex.search(line)

		#If we found a match...
		if cluster_match:
			#Rename to cluster_id for readabilty.
			cluster_id = int(cluster_match.group())

			#If new cluster_id, create a new dictionary 
			#key with a list as a value.
			if cluster_id not in clusters:
				clusters[cluster_id] = list()

			#Match for the song name.
			song_match = song_regex.match(line)

			#If we found a song match...
			if song_match:
				#Rename to song_name for readability.
				song_name = song_match.group()
				#Add song to corresponding cluster list.
				clusters[cluster_id].append(song_name)
			else:
				#We should never reach this.
				sys.exit("ABORTED: Did not find song in line: " + line)

	return clusters

if __name__ == '__main__':
	print "Using cluster group data in file: " + CLUSTER_GROUP_FILE
	print "Using input data in file: " + ALL_DATA_FILE
	#Get data from cluster group file.
	data = read_file(CLUSTER_GROUP_FILE)
	#Group songs into clusters.
	clusters = build_clusters(data)

	#Create csv files:

	#For each cluster...
	for cluster_id in clusters:
		#First, open the input file
		with open(ALL_DATA_FILE, 'rb') as csv_in:
			reader = csv.reader(csv_in)
			#Second, create an output file
			with open(OUTPUT_FILE_PREFIX + str(cluster_id + 1) + "of" + str(len(clusters)) + ".csv", 'wb') as csv_out:
				writer = csv.writer(csv_out)
				#Finally, for each row in the input file...
				for row in reader:
					#...if there's valid data in the row...
					if row:
						#...and if the row has data matching the current cluster...
						if row[0] in clusters[cluster_id]:
							#then write the data into the current cluster's output file.
							writer.writerow(row)
				print "Created cluster in file: " + OUTPUT_FILE_PREFIX + str(cluster_id + 1) + "of" + str(len(clusters)) + ".csv"
	print "Done!"