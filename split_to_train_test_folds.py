#!/usr/bin/env python
import math
import subprocess
import os
import csv

folds = open('all_folds.tsv','r')
folds_reader = csv.reader(folds, dialect=csv.excel_tab)

for i in range (1,11):

	to_split = open('all_to_split','r')
	to_split_reader = csv.reader(to_split, dialect=csv.excel_tab)
	header = to_split_reader.next()
	
	try:
		test_queries = folds_reader.next()
	except StopIteration:
		x=1
	
	test = open('all_test'+str(i)+'.csv', 'wb')
	test_writer = csv.writer(test,dialect=csv.excel)
	test_writer.writerow(header[2:])

	train = open('all_train'+str(i)+'.csv', 'wb')
	train_writer = csv.writer(train,dialect=csv.excel)
	train_writer.writerow(header[2:])

	line = to_split_reader.next()
	curr_query = line[1]
	prev_query = curr_query
	while line:
	
		if str(int(curr_query.strip())) in test_queries:
			if line[0] == '1':
				test_writer.writerow(line[2:])
		else:
			train_writer.writerow(line[2:])
		try:
			line = to_split_reader.next()
		except StopIteration:
			break
		curr_query = line[1]
		if curr_query and prev_query != curr_query:
			prev_query = curr_query	
				
	train.close()
	test.close()	
	to_split.close()			