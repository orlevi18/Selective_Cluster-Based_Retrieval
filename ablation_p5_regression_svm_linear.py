#!/usr/bin/env python
import math
import csv
import os
import subprocess

import sys

classifier="smo_linear"
eval ="p5_reg_robust"
input_file = open(sys.argv[1], 'r')
input_set = eval+"_"+classifier+"_"+input_file.name



if not os.path.exists("test_"+input_set):
    os.makedirs("test_"+input_set)	

for setline in input_file:
	setnum = setline.split(" ")[0].strip()
	start_remove_in= setline.split(" ")[1].split(",")
	start_remove_in=filter(None, start_remove_in)
	start_remove_in = [int(mm) for mm in start_remove_in]
	start_remove = []			
	for feat in range(2,41):
		if feat not in start_remove_in:
			start_remove.append(str(feat))
	
	result = open("result_"+input_set+"_"+str(setnum),'w')
	log = open("log_"+input_set+"_"+str(setnum),'w')
	test_to_run = open("test_to_run_"+input_set+"_"+str(setnum),'w')
	#print start_remove
	
	iter=0

	features = []
	for test_fold in range(0,11):
		features.insert(test_fold,start_remove+[])
	
	grade={}
	for test_fold in range(1,11):
		grade[test_fold]=0
		
	check = 1	
	check_stop = {}
	for test_fold in range(1,11):
		check_stop[test_fold]=1
	
	while check==1:
		
		for test_fold in range(1,11):
			if check_stop[test_fold]==0:
				continue
			for valid_fold in range(1,10):
				for feat in range(2,41):
					if iter==0:
						if feat > 2: 
							continue
						else:
							feat = 1
					else:
						if str(feat) in features[test_fold]:
							continue
					x="java -Xmx1000M -cp weka.jar weka.classifiers.meta.FilteredClassifier -t \"in_"+eval+"/all_train"+str(test_fold)+"_"+str(valid_fold)+".arff\" -T \"in_"+eval+"/all_valid"+str(test_fold)+"_"+str(valid_fold)+".arff\" -p 1"
					x+=" -F \"weka.filters.MultiFilter -F \\\"weka.filters.unsupervised.attribute.ReplaceMissingValues\\\"" 
					x+=" -F \\\"weka.filters.unsupervised.attribute.Normalize -S 1.0 -T 0.0\\\""
					x+=" -F \\\"weka.filters.unsupervised.attribute.Remove -R "+','.join(features[test_fold])+","+str(feat)+" \\\"\"" 
					x+=" -W weka.classifiers.functions.SMOreg" 
					x+=" -- -C 1.0 -N 0 -I \"weka.classifiers.functions.supportVector.RegSMOImproved -T 0.001 -V -P 1.0E-12 -L 0.001 -W 1\" "
					x+=" -K \"weka.classifiers.functions.supportVector.PolyKernel -E 1.0 -C 250007\" > 'test_"+input_set+"/svm_reg_out"+str(test_fold)+"_"+str(valid_fold)+"_"+str(feat)+"_"+str(iter)+".txt'"
					#print str(x)
					print str(test_fold) + " " + str(valid_fold) + " " + str(feat) + " " + str(iter)
					log.write(str(test_fold) + " " + str(valid_fold) + " " + str(feat) + " " + str(iter)+"\n")
					p = subprocess.Popen(x, stdout=subprocess.PIPE, shell=True)
					(output, err) = p.communicate()
		

		max_feat = {}
		max_grade = {}
		check = 0

		for test_fold in range(1,11):		# test
			if check_stop[test_fold]==0:
				continue
			perform = {}
			for feat in range(2,41):
			#for feat in range(0,1):
				if iter==0:
					if feat > 2: 
						continue
					else:
						feat = 1
				else:
					if str(feat) in features[test_fold]:
						continue
				perform[feat]=0
			
			for valid_fold in range(1,10):	# valid
				
				valids = open("in_"+eval+"/queries_valid"+str(test_fold)+"_"+str(valid_fold)+'.csv','r')
				valids_reader = csv.reader(valids)
				test_queries = valids_reader.next()
				
				test_queries=filter(None, test_queries)
				test_queries = [int(mm) for mm in test_queries]
				
				for feat in range(2,41):
				#for feat in range(0,1):
					if iter==0:
						if feat > 2: 
							continue
						else:
							feat = 1
					else:
						if str(feat) in features[test_fold]:
							continue
					
					prediction = open("test_"+input_set+"/svm_reg_out"+str(test_fold)+"_"+str(valid_fold)+"_"+str(feat)+"_"+str(iter)+'.txt','r')
					p5file = open('in_'+eval+'/all_p5','r')
					p5sum = 0.0
					
					for p5line in p5file:
						query = int(p5line.split("\t")[0].strip())
						qlp5 = float(p5line.split("\t")[1].strip())
						mrfp5 = float(p5line.split("\t")[2].strip())
						
						if query in test_queries:
						
							line = prediction.readline()
							while line.find("(")==-1 or line.find("#")!=-1:
								line = prediction.readline()

							line = line.split(" ")
							pp = 0
							while line[pp] == "":
								pp = pp + 1
							pp = pp + 1
							while line[pp] == "":
								pp = pp + 1
							actual = line[pp]
							pp = pp + 1
							while line[pp] == "":
								pp = pp + 1
							predicted = line[pp]
										
							try:
								predicted = float(predicted)
							except ValueError:
								predicted = 0.0
								
							if float(predicted) > 0:
								p5sum = p5sum + qlp5
							else:
								p5sum = p5sum + mrfp5
									
							
					perform[feat]=perform[feat]+p5sum
					prediction.close()
					p5file.close()	

				valids.close()
			
			m=1
			n=0
			for p in sorted(perform,key=perform.get,reverse=True):	
				n=n+1
				if n==1:
					max_feat[test_fold]=p
					max_grade[test_fold]=perform[p]
				print str(test_fold) + " " + str(p) + " " + str(perform[p])
			
		for test_fold in range(1,11):
			if check_stop[test_fold]==0:
				continue
			print str(iter) + " " + str(test_fold) + ' ' + str(max_grade[test_fold]) + " " + str(grade[test_fold]) + " " + str(max_feat[test_fold]) + " "
			log.write(str(iter) + " " + str(test_fold) + ' ' + str(max_grade[test_fold]) + " " + str(grade[test_fold]) + " " + str(max_feat[test_fold])+"\n")
			if max_grade[test_fold]>grade[test_fold]:
				grade[test_fold] =  max_grade[test_fold]
				features[test_fold].append(str(max_feat[test_fold]))
				check = 1
				print "added feature " + str(max_feat[test_fold])
				log.write("added feature " + str(max_feat[test_fold])+"\n")
			else:
				check_stop[test_fold]=0

		print features
		
		print "************completed iter " + str(iter) + " ***********************"
		log.write("************completed iter " + str(iter) + " ***********************"+"\n")
		iter=iter+1

	print "************finished iterations***********************"	
	log.write("************finished iterations***********************"	+"\n")
		
	for test_fold in range(1,11):
			
		x="java -Xmx1000M -cp weka.jar weka.classifiers.meta.FilteredClassifier -t \"in_"+eval+"/all_train"+str(test_fold)+".arff\" -T \"in_"+eval+"/all_test"+str(test_fold)+".arff\" -p 1"
		x+=" -F \"weka.filters.MultiFilter -F \\\"weka.filters.unsupervised.attribute.ReplaceMissingValues\\\"" 
		x+=" -F \\\"weka.filters.unsupervised.attribute.Normalize -S 1.0 -T 0.0\\\""
		x+=" -F \\\"weka.filters.unsupervised.attribute.Remove -R "+','.join(features[test_fold])+" \\\"\"" 
		x+=" -W weka.classifiers.functions.SMOreg" 
		x+=" -- -C 1.0 -N 0 -I \"weka.classifiers.functions.supportVector.RegSMOImproved -T 0.001 -V -P 1.0E-12 -L 0.001 -W 1\" "
		x+=" -K \"weka.classifiers.functions.supportVector.PolyKernel -E 1.0 -C 250007\" > 'test_"+input_set+"/svm_reg_out"+str(test_fold)+".txt'"
		
		test_to_run.write(x+"\n\n")
		p = subprocess.Popen(x, stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
		

	totalp5 = {}
	totalp5['111']=0
	totalp5['222']=0
	totalp5['333']=0
	totalp5['444']=0
	totalp5['555']=0
	count = {}
	count['111']=0.0
	count['222']=0.0
	count['333']=0.0
	count['444']=0.0
	count['555']=0.0
	correct_count = {}
	correct_count['111']=0
	correct_count['222']=0
	correct_count['333']=0
	correct_count['444']=0
	correct_count['555']=0

	folds = open('in_'+eval+'/all_folds.tsv','r')
	folds_reader = csv.reader(folds, dialect=csv.excel_tab)

	for fold in range (1,11):
		prediction = open("test_"+input_set+"/svm_reg_out"+str(fold)+".txt",'r')	
		test_queries = folds_reader.next()
		test_queries = filter(None,test_queries)	
		test_queries = [ int(x) for x in test_queries ]
		p5file = open('in_'+eval+'/all_p5','r')
		for p5line in p5file:
			query = p5line.split("\t")[0]	
			dataset = query[0:3]
			qlp5 = float(p5line.split("\t")[1].strip())
			mrfp5 = float(p5line.split("\t")[2].strip())

			if int(query) in test_queries:
				
				line = prediction.readline()
				while line.find("(")==-1 or line.find("#")!=-1:
					line = prediction.readline()

				line = line.split(" ")
				pp = 0
				while line[pp] == "":
					pp = pp + 1
				pp = pp + 1
				while line[pp] == "":
					pp = pp + 1
				actual = line[pp]
				pp = pp + 1
				while line[pp] == "":
					pp = pp + 1
				predicted = line[pp]
							
				try:
					predicted = float(predicted)
				except ValueError:
					predicted = 0.0
				#print query + " " + line		
				if float(predicted) > 0:
					totalp5[dataset] = totalp5[dataset] + qlp5
					correct = qlp5
				else:
					totalp5[dataset] = totalp5[dataset] + mrfp5
					correct = mrfp5
					
				count[dataset] = count[dataset] + 1.0

				if correct >= qlp5 and correct >= mrfp5:
					correct_count[dataset] = correct_count[dataset] + 1
		
		p5file.close()					
		prediction.close()

	result.write(setnum)	
	for dataset in totalp5:	
		result.write("\t"+str(totalp5[dataset]/count[dataset]))
	result.write("\n")
	test_to_run.close()
	result.close()
	log.close()
	folds.close()

input_file.close()

	