#!/bin/bash

#
# A simple bash script that parses the corpus, gets probabilities by phrase position,
# and writes csvs
#

python parse.py # parse.py is set to output a file 'example.csv'
python 4Bars_0thPower.py example.csv
python 4Bars_PerSong_EachBar.py example.csv
python confidence.py
