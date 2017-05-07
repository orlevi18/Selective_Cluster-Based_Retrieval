#!/usr/bin/env python
import math
import subprocess
import os

num_of_terms = [5,10,25,50,100]
beta = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

num_of_queries = 97
logger = open('loggerrm3','w')
rm3rank = open('rm3rank','w')

for loo in range(1,num_of_queries+1):
	print(loo)
	max = -1
	max_terms = 0
	max_beta = 0
	for i in range(0,5):
		for b in range(0,11):
			logger.write("loo: "+str(loo)+" "+str(num_of_terms[i])+" "+str(beta[b])+"\n")
			
			eval = open('./wt10g_top_5_ql/eval_'+str(num_of_terms[i])+'_'+str(beta[b]),'r')
			sum=0.0
			for j in range(1,20):
					line = eval.readline()
			for o in range(1,num_of_queries+1):
				if o!=loo:
					test_p5 = line.split('\t')[0].strip()
					if test_p5!="P5":
						print("error\nerror\nerror\n")
					p5 = float(line.split('\t')[2].strip())
					sum = sum + p5
					logger.write("other: "+str(o)+" "+str(p5)+"\n")
				if o==loo:
					curr_query = line.split('\t')[1].strip()
				for j in range(1,28):
					line = eval.readline()	
				
			avg = sum/float(num_of_queries-1)
			logger.write("avg: "+str(loo)+"      "+str(avg)+"\n")
			if avg > max:
				max=avg
				max_terms = num_of_terms[i]
				max_beta = beta[b]
			
			eval.close()
			
	logger.write("max: "+str(max)+" "+str(max_terms)+" "+str(max_beta)+"\n")
	
	res = open('./wt10g_top_5_ql/out_'+str(max_terms)+'_'+str(max_beta),'r')
	line = res.readline()
	while line.split(' ')[0]!=curr_query:
		line = res.readline()
	while line.split(' ')[0]==curr_query:
		rm3rank.write(line)
		line = res.readline()
	res.close()
	
rm3rank.close()
logger.close()		
	
			
