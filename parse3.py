#Parser3.py

#INCOMPLETE PARSER, work in progress!

# This parser get a list of all the songs in the billboard, and for each song it
# extracts the entire text as a string, and splits it by whitespace, essentially
# creating an array of only the smallest parts possible to describe the song.
# The parser then goes part by part, deciding what to do with each one. Instead of
# incrementing the index after each part, we pop ("remove") them and look at the 
# next part in the front of the array; we shrink the array as we parse until it
# is gone. After we finish parsing the array, we move on to the next song. Rinse
# and repeat until we are done.

from __future__ import division

import os
import re
import csv
import sys

from collections import defaultdict, deque

CSV_FILE = "example1.csv"
ROOT_DIR = "McGill-Billboard"

KEYS = [{'A'}, {'A#', 'Bb'}, {'B', 'Cb'}, {'C'}, {'C#', 'Db'}, {'D'}, {'D#', 'Eb'}, {'E', 'Fb'}, {'F'}, {'F#', 'Gb'}, {'G'}, {'G#', 'Ab'}]
RN = ['I', 'bII', 'II', 'bIII', 'III', 'IV', 'bV', 'V', 'bVI', 'VI', 'bVII', 'VII']

def lookup_chord(key, key_list):
    """Look up the numerical position of a chord root relative to an ordered list of roots (possibly shifted)."""
    for i, k in enumerate(key_list):
        if key in k:
            return i

"""Use the tonic to convert given chords to roman numerals"""
def get_roman(tonic, chord):
    root_num = lookup_chord(tonic, KEYS)
    shifted_keys = deque(KEYS)
    shifted_keys.rotate(-root_num)
    return RN[lookup_chord(chord, shifted_keys)]

"""open up a file and return an array containing splitted text"""
def readfile(name):
	with open(name, "r") as file:		#Open file
		data = file.read()				#get the data
		data = re.split(r'\s', data)	#Split by whitespace, put in array
		return data

def main():

	#Write to csv file.
	with open(CSV_FILE, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		
		#Get all the salami_chords files.
		songs = [os.path.join(* [ROOT_DIR, sub_dir, 'salami_chords.txt']) for sub_dir in os.listdir(ROOT_DIR)]

		for song in sorted(songs):
			title = ""
			tonic = ""

			data = readfile(song)	#Get the data from a song

			#THE PARSER
			while len(data) > 0:	#Parse each element of said song

				#Matched song title
				if re.match(r'title:', data[0]):
					data.pop(0)
					while data[0] is not "#":		#Get the title of the song
						title = title + data.pop(0) + " "
					title = title[:-1]				#Remove leftover space in title

				#Matched artist
				elif re.match(r'artist:', data[0]):
					data.pop(0)						#Ignore artist
					while data[0] is not "#":
						data.pop(0)

				#Matched metre
				elif re.match(r'metre:', data[0]):	#Ignore metre
					data.pop(0)
					data.pop(0)

				#Matched tonic
				elif re.match(r'tonic:', data[0]):	#Get tonic
					data.pop(0)
					tonic = data.pop(0)

				#Matched form content
				elif re.match(r'[A-Z],', data[0]):	#Get form_content
					form_content = data.pop(0)[:-1]

				#Matched form function
				elif re.match(r'^[a-z]+-*[a-z]*,*$', data[0]): #Get form_function
					form_function = data.pop(0)[:-1]

				#Matched bar
				elif re.match(r'\|', data[0]):		#increment current bar count
					current_bar += 1
					data.pop(0)

				#Matched chord
				elif re.match(r'[A-G](b*|#*):.+', data[0]):
					original_chord = data.pop(0)					#Get the current chord
					split_chord = re.split(r':', original_chord)	#split chord and chord quality
					roman_chord = get_roman(tonic, split_chord[0]) 	#Convert chord to roman numeral
					chord_quality = split_chord[1]					#Get chord quality

					if re.match(r'->', data[1]):	#check for arrow (What is that called, again?)
						arrow = 1

					#WRITE A CSV LINE
					writer.writerow([title,form_content,form_function,original_chord,roman_chord,chord_quality,current_bar,total_bars, arrow])

				#Matched . (Repeat previous chord)
				elif re.match(r'^\.$', data[0]):
					data.pop(0)
					if re.match(r'->', data[1]):	#check for arrow (What is that called, again?)
						arrow = 1

					#WRITE A CSV LINE
					writer.writerow([title,form_content,form_function,original_chord,roman_chord,chord_quality,current_bar,total_bars, arrow])

				#Matched time
				elif re.match(r'(\d+\.\d+)',data[0]):
					#ignore time, but use it to reset arrow and current_bar.
					#We also use it to count up the total bars in the upcoming phrase.
					current_bar = 0
					arrow = 0

					i = 1
					total_bars = -1 #(total_bars is always the number of pipes minus 1)
					while not re.match(r'(\d+\.\d+)',data[i]): #search for bars until we reach the next phrase.
						if re.match(r'\|', data[i]): #found a bar, count it.
							total_bars += 1
						if re.match(r'end',data[i]):	#prevent ourselves from looking beyond the data array.
							break
						i += 1
					data.pop(0)

				#Matched other things to ignore (#, empty strings, silence, end, instrumentation, arrow)
				#(We ignore the arrow because it has already been accounted for.)
				elif re.match(r'#|\Z|silence|end|^\(*[a-z]+\)*,*$|->', data[0]):
					data.pop(0)

				#The regular expressions below are those that data still needs to be
				#matched to. Uncommenting the elif makes the parser run through ALL the songs.
				elif re.match(r'^x\d+,*$|N|\(\d/\d\)|[A-Z]\'*|&pause|^\*$', data[0]):
					data.pop(0) #Ignore for testing purposes.
				
				#Did not match	
				else:
					#We are not meant to get here. Something went wrong.
					sys.exit("Aborted! Could not parse: " + data[0] + " (" + song + ")")
					
			print "Parsed \"" + title + "\" (" + song + ")"
		print "Finished parsing! Data written to csv file: " + CSV_FILE

if __name__ == '__main__':
	main()