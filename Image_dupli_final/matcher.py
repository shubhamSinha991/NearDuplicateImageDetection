import numpy as np
import h5py

import os,sys
from os.path import isfile, join
from random import randint
from shutil import copyfile

from siglib import createSignature, compareSignature
from comparator import Comparator
from bucket import Bucket

def makeDir(path):
	if not os.path.exists(path):
	    os.mkdir(path)
	return


comparator = Comparator()

#folder for dataset images
input_path = 'images'
output_path = 'out'
critial_match = 15 #30 percent

#scan the input files
onlyfiles = [ f for f in os.listdir(input_path) if isfile(join(input_path,f)) ]

#Add the first image in the first bucket
buckets = [Bucket(onlyfiles[0],comparator.createSign(join(input_path,onlyfiles[0])))]

for fileindex in range(1, len(onlyfiles)):
	print onlyfiles[fileindex]
	sign_t = comparator.createSign(join(input_path,onlyfiles[fileindex]))
	#print sign_t
	matched_bucket = None
	match = critial_match
	for b in buckets:
		#print "Bucket #"+str(b.bid)+" size:"+str(b.size)
		nmatch = compareSignature(b.getSign(),sign_t)
		#print "match = "+str(nmatch*2)+"%"
		if(nmatch>=match):
			matched_bucket = b	#Chooses the bucket with best match
			
	#Now if best match is found then add it to the corresponding bucket or
	#create a new bucket
	
	if(matched_bucket==None):
		print "creating new bucket"
		b = Bucket(onlyfiles[fileindex],sign_t)
		buckets.append(b)				
	else:
		print "adding to bucket #"+str(matched_bucket.bid)
		matched_bucket.addSign(onlyfiles[fileindex],sign_t)
		
	
print "End results : "
makeDir(output_path)

for b in buckets:
	print "Bucket #"+str(b.bid)+" size:"+str(b.size)
	print b.image_list
	
	if(b.size>1):
		makeDir(join(output_path,"bucket"+str(b.bid)))
		for img in b.image_list:
			copyfile(join(input_path,img),join(output_path,"bucket"+str(b.bid),img))
	else:
		copyfile(join(input_path,b.image_list[0]),join(output_path,b.image_list[0]))
	


