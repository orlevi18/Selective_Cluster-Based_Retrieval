#!/usr/bin/env python
import math
import subprocess
import os

svm_out = open('svm_out','w')

for docs_in_cluster in range (5,6):

	clusters_file = 'clusters_'+str(docs_in_cluster)
	clusters = open(clusters_file, 'r')
	clust_line = clusters.readline()

	ql1 = open("initQL", 'r')
	ql1_line = ql1.readline()
	ql2 = open("initQL", 'r')
	ql2_line = ql2.readline()

	svm_ranking = open("svm_ranking", 'r')	
	for svm_ranking_line in svm_ranking:

		curr_query = svm_ranking_line.split(' ')[0]
		top_cluster = svm_ranking_line.split(' ')[1].strip()
		
		docs = []
		while clust_line.split(' ')[0] == curr_query:
			cluster = clust_line.split(' ')[1].strip()
			if cluster == top_cluster:		
				docs = clust_line.split(' ')
				docs = docs[3:]
				docs = [x.strip() for x in docs]
			clust_line = clusters.readline()
			
		# find the lines of the docs of the top cluster
			
		lines = []
		j=0
		while ql1_line.split(' ')[0] == curr_query:
			doc = ql1_line.split(' ')[2]
			if doc in docs and j<docs_in_cluster:
				lines.append(ql1_line)	
				j=j+1				
			ql1_line = ql1.readline()	
		
		index = 1
		
		for line in lines:
			lst = line.split(' ')
			lst[3] = str(index)
			lst[4] = str(index*(-1))
			index = index + 1
			line = ' '.join(lst)
			svm_out.write(line)
		
		while ql2_line.split(' ')[0] == curr_query:
			if ql2_line not in lines:
				lst = ql2_line.split(' ')
				lst[3] = str(index)
				lst[4] = str(index*(-1))
				index = index + 1
				ql2_line = ' '.join(lst)
				svm_out.write(ql2_line)
				
			ql2_line = ql2.readline()	
			
	svm_ranking.close()
	clusters.close()
	ql1.close()
	ql2.close()
	
svm_out.close()