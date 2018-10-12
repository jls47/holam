import csv
import urllib.request
import pandas as pd

def compare(fname1, fname2):
	data1 = []
	data2 = []
	with open(fname1) as csvfile:
		reader = pd.read_csv(fname1)
		data = reader
		
		print(data)
		for thing in data:
			data1.append(thing)
			
	with open(fname2) as csvfile:
		reader = pd.read_csv(fname1)
		data = reader
		
		print(data)
		for thing in data:
			data2.append(thing)
	print(data1)
	print(data2)

		
compare('try1.csv', 'try2.csv')