#!/usr/bin/env python

import csv

dictQL = {}
dictMRF = {}
dictQRELS = {}

initQL = open('initQL_50','r')

outp5 = open('outp5','w')

for lineQL in initQL:
	keyQL = lineQL.split(' ')[0] + " " + lineQL.split(' ')[2]
	dictQL[keyQL] = lineQL.split(' ')[3]
initQL.close()

MRF = open('clustmrf.documents_5_50','r')	
for lineMRF in MRF:
	keyMRF = lineMRF.split(' ')[0] + " " + lineMRF.split(' ')[2]
	dictMRF[keyMRF] = lineMRF.split(' ')[3]
MRF.close()

qrels = open('qrels','r')	
for lineQRELS in qrels:
	keyQRELS = lineQRELS.split(' ')[0] + " " + lineQRELS.split(' ')[2]
	dictQRELS[keyQRELS] = lineQRELS.split(' ')[3]
qrels.close()

folds = open('C:/cygwin64/home/olevi/split/robust_folds.tsv','r')
folds_reader = csv.reader(folds, dialect=csv.excel_tab)

finalp5=0.0
finalcount=0
for fold in range (1,11):
	
	test_queries = folds_reader.next()
	test_queries = filter(None,test_queries)	
	test_queries = [ int(x) for x in test_queries ]
	
	maxk = 0
	maxp5 = 0.0
	
	for krank in (60, 60):
		dictFUSED = {}
		for keyQL in dictQL:
			dictFUSED[keyQL]=(1/(float(dictQL[keyQL])+krank)) + (1/(float(dictMRF[keyQL])+krank))

		dictFUSEDquery = {}
		totalp5 = 0.0
		prev="301"
		for keyQL in sorted(dictQL):
			#print keyQL
			query=keyQL.split(' ')[0]
			if query!=prev:
				c=0
				for keyFUSEDquery in sorted(dictFUSEDquery,key=dictFUSEDquery.get,reverse=True):
					if c>=5: 
						break
					c=c+1
					#print prev + " " + keyFUSEDquery + " " + str(dictFUSEDquery[keyFUSEDquery])
					q = dictQRELS.get(prev + " " + keyFUSEDquery,"empty")
					if q != "empty" and float(q) > 0 and int(prev) not in test_queries:
						totalp5 += 1
				#print prev + " " + str(p5/5.0)
				dictFUSEDquery = {}
				prev=query
			doc=keyQL.split(' ')[1]
			dictFUSEDquery[doc]=dictFUSED[keyQL]
			
		c=0
		for keyFUSEDquery in sorted(dictFUSEDquery,key=dictFUSEDquery.get,reverse=True):
			if c>=5: 
				break
			c=c+1
			#print prev + " " + keyFUSEDquery + " " + str(dictFUSEDquery[keyFUSEDquery])
			q = dictQRELS.get(prev + " " + keyFUSEDquery,"empty")
			if q != "empty" and float(q) > 0 and int(prev) not in test_queries:
				totalp5 += 1
		#print prev + " " + str(p5/5.0)

		if totalp5 > maxp5:
			maxp5=totalp5
			maxk = krank
		
		
			
	dictFUSED = {}
	for keyQL in dictQL:
		dictFUSED[keyQL]=(1/(float(dictQL[keyQL])+maxk)) + (1/(float(dictMRF[keyQL])+maxk))

	dictFUSEDquery = {}
	p5 = 0.0
	prev="301"
	for keyQL in sorted(dictQL):
		#print keyQL
		query=keyQL.split(' ')[0]
		if query!=prev:
			c=0
			for keyFUSEDquery in sorted(dictFUSEDquery,key=dictFUSEDquery.get,reverse=True):
				if c>=5: 
					break
				c=c+1
				#print prev + " " + keyFUSEDquery + " " + str(dictFUSEDquery[keyFUSEDquery])
				q = dictQRELS.get(prev + " " + keyFUSEDquery,"empty")
				if q != "empty" and float(q) > 0 and int(prev) in test_queries:
					p5 += 1
			if int(prev) in test_queries:
				outp5.write(prev + " " + str(p5/5.0)+'\n')
				finalp5+=p5/5.0
				finalcount+=1
			p5 = 0.0
			dictFUSEDquery = {}
			prev=query
		doc=keyQL.split(' ')[1]
		dictFUSEDquery[doc]=dictFUSED[keyQL]
		
	c=0
	for keyFUSEDquery in sorted(dictFUSEDquery,key=dictFUSEDquery.get,reverse=True):
		if c>=5: 
			break
		c=c+1
		#print prev + " " + keyFUSEDquery + " " + str(dictFUSEDquery[keyFUSEDquery])
		q = dictQRELS.get(prev + " " + keyFUSEDquery,"empty")
		if q != "empty" and float(q) > 0 and int(prev) in test_queries:
			p5 += 1
	if int(prev) in test_queries:
		outp5.write(prev + " " + str(p5/5.0)+'\n')
		finalp5+=p5/5.0
		finalcount+=1
		
print str(finalp5/finalcount) + " " + str(finalcount)

