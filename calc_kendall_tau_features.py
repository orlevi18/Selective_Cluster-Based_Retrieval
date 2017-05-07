#!/usr/bin/env python
import math
import subprocess
import os

logger = open('logger','w')

for i in range(1,11):
	set = 'test'+str(i)
	print(set)
	trans = open('trans_'+set,'r')
	
	allfeatures = open('svmrank_'+set,'w')
	
	tworows = open("new_features_2rows","r")
	mrf_features = tworows.readline()
	
	rm3ql = open('rm3ql','r')
	rm3ql_line = rm3ql.readline()
	rm3mrf = open('rm3mrf','r')
	rm3mrf_line = rm3mrf.readline()
	
	line = trans.readline()
	curr_query = line.split(' ')[0]
	prev_query=curr_query
	mrf = open('mrf','w')
	
	while line:
		mrf.write(line.split(' ')[1])
		line = trans.readline()
		curr_query = line.split(' ')[0]
		if curr_query != prev_query:
			rm3 = open('rm3','w')
			while rm3ql_line.split(' ')[0] != prev_query:
				rm3ql_line = rm3ql.readline()
			while rm3ql_line.split(' ')[0] == prev_query:
				rm3.write(rm3ql_line.split(' ')[2]+"\n")
				rm3ql_line = rm3ql.readline()
			rm3.close()
			mrf.close()
			rboql = float(subprocess.check_output(['./rbo','-m','rbo','./mrf','./rm3']))
			kendallql = float(subprocess.check_output(['./rbo','-m','tau','./mrf','./rm3']))
			
			rm3 = open('rm3','w')
			while rm3mrf_line.split(' ')[0] != prev_query:
				rm3mrf_line = rm3mrf.readline()
			while rm3mrf_line.split(' ')[0] == prev_query:
				rm3.write(rm3mrf_line.split(' ')[2]+"\n")
				rm3mrf_line = rm3mrf.readline()
			rm3.close()
			rbomrf = float(subprocess.check_output(['./rbo','-m','rbo','./mrf','./rm3']))
			kendallmrf = float(subprocess.check_output(['./rbo','-m','tau','./mrf','./rm3']))
			
			logger.write(set + ' ' + prev_query + ' ' + str(rboql) + ' ' + str(kendallql) + ' ' + str(rbomrf) + ' ' + str(kendallmrf) + '\n')
			
			frboql = math.log(math.exp(rboql)+math.pow(10,-10))
			frbomrf = math.log(math.exp(rbomrf)+math.pow(10,-10))
			ftauql = math.log(math.exp(kendallql)+math.pow(10,-10))
			ftaumrf = math.log(math.exp(kendallmrf)+math.pow(10,-10))
			
			while mrf_features.split(' ')[1].split(':')[1] != prev_query:
				mrf_features = tworows.readline()
				
			mrf_features = mrf_features.replace("#",'22:'+str(frboql)+' 23:'+str(ftauql)+' #')
			allfeatures.write(mrf_features)
			
			mrf_features = tworows.readline()	
			mrf_features = mrf_features.replace("#",'22:'+str(frbomrf)+' 23:'+str(ftaumrf)+' #')
			allfeatures.write(mrf_features)
			
			prev_query=curr_query
			mrf = open('mrf','w')
	
	mrf.close()
	rm3ql.close()
	rm3mrf.close()
	trans.close()
	
logger.close()