from __future__ import division

import os
import re
import csv

from collections import defaultdict, deque

ROOT_DIR = 'McGill-BillboardSample'

KEYS = [{'A'}, {'A#', 'Bb'}, {'B', 'Cb'}, {'C'}, {'C#', 'Db'}, {'D'}, {'D#', 'Eb'}, {'E', 'Fb'}, {'F'}, {'F#', 'Gb'}, {'G'}, {'G#', 'Ab'}]
RN = ['I', 'bII', 'II', 'bIII', 'III', 'IV', 'bV', 'V', 'bVI', 'VI', 'bVII', 'VII']

def lookup_chord(key, key_list):
    """Look up the numerical position of a chord root relative to an ordered list of roots (possibly shifted)."""
    for i, k in enumerate(key_list):
        if key in k:
            return i

def corpus_list(root):
    """Return a list of all paths to the salami text files, relative to the root directory of the project."""
    return [os.path.join(* [root, sub_dir, 'salami_chords.txt']) for sub_dir in os.listdir(root)]


def get_tonic(f):
    fs = open(f)
    line = fs.readline()
    while 'tonic' not in line:
        line = fs.readline()
    tonic = line[line.index(':') + 2:-1]
    return tonic

def get_chord_sequence(line):
    """
    Return a list of chord sequences from a line.
    """
    return re.findall(r'\S+:\S+', line)


def get_relative(tonic, chords):
    """
    Return a list of the relative root numbers based on the tonic note and
    a list of absolute chords. Returns integers, where 0 -> I, 1 -> II, etc.

    TODO: needs testing and verification that it is working properly

    """
    root_num = lookup_chord(tonic, KEYS)
    shifted_keys = deque(KEYS)
    shifted_keys.rotate(-root_num)
    relative_chords = []
    for c in chords:
        root, quality = c.split(':')
        relative_chords.append(RN[lookup_chord(root, shifted_keys)])
    return relative_chords

def update_form(previous_form, line):
	regex = re.compile("\w+,|\w+',")
	newform = regex.findall(line)
	if newform:
		if len(newform) == 1:
			newform.insert(0,"")
		return [newform[0].replace(",",""), newform[1].replace(",","")]
	else:
		return previous_form

def get_chord_quality(chordList):
	return [x.split(":")[1] for x in chordList]

def get_bar_in_phrase(line):
	barNumbersList = []
	barlist =  line.split("|")[1:-1]	
	for index, bar in enumerate(barlist):
		chordsInBar = get_chord_sequence(bar)
		barNumbersList += [index + 1]*len(chordsInBar)

	return barNumbersList

def get_total_bars(barNumbersList):
	if barNumbersList: return barNumbersList[len(barNumbersList) -1]		

def get_title(song):
    fs = open(song)
    line = fs.readline()
    while 'title' not in line:
        line = fs.readline()
    title = line[line.index(':') + 2:-1]
    return title

def get_arrow(line):
	if "->" in line:
		return 1
	else:
		return 0

def get_repeats(line):
	repeats = re.findall(r'x+\d',line)		
	if repeats: 
		return int(repeats[0][-1])	
	else:
		return 1

if __name__ == '__main__':
    """Write an example csv to play with for the analysis code."""
    filenames = corpus_list(ROOT_DIR)
    relative_chords = []

    with open('example.csv', 'wb') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    	for song in filenames:
		                       
		Tonic = get_tonic(song)
		fs=open(song)
		formFunc = []
	
		arrowList = []	
		titleList = []
		chordList = []
		relativeChordList = []
		barNumbers = []
		totalBarNumbers = []
		formFuncList = []
		formLetterList = []
		chordQualityList = []

		for line in fs:
			chordsInPhrase =  get_chord_sequence(line)			
			relativeChords =  get_relative(Tonic,chordsInPhrase)

			
 			title = [get_title(song).replace(" ","")]*len(chordsInPhrase)
			barInPhrase = get_bar_in_phrase(line)	
			totalInPhrase = [get_total_bars(barInPhrase)]*len(chordsInPhrase)
			phraseFormFunc = []
			formLetter = [] 		
			formFunc =  update_form(formFunc,line)
			print formFunc
			if formFunc: phraseFormFunc = [formFunc[1]]*len(chordsInPhrase)
			if formFunc: formLetter = [formFunc[0]]*len(chordsInPhrase)
			chordQualities = get_chord_quality(chordsInPhrase)	
			arrows = [0]*len(chordsInPhrase)
			if arrows: arrows[-1] = get_arrow(line)
			repeats = get_repeats(line)

			titleList += title*repeats
			chordList +=  chordsInPhrase*repeats
			relativeChordList += relativeChords*repeats
			barNumbers +=  barInPhrase*repeats
			totalBarNumbers +=  totalInPhrase*repeats
			formFuncList += phraseFormFunc*repeats
			formLetterList += formLetter*repeats
			chordQualityList += chordQualities*repeats
			arrowList += arrows*repeats 	

		for title, form, letter, chord, interval, quality, num, total, arrows in zip(titleList, formFuncList,formLetterList,chordList,relativeChordList,chordQualityList,barNumbers,totalBarNumbers,arrowList):
			writer.writerow([title, form,letter,chord,interval,quality,num,total,arrows])
		writer.writerow([]) 


