import numpy as np
import h5py
from sklearn.metrics.pairwise import euclidean_distances
from os import listdir
from os.path import isfile, join
import cv2
from shutil import copyfile
import os,sys
from math import log10

from comparator import Comparator
from bucket import Bucket


def makeDir(path):
	if not os.path.exists(path):
	    os.mkdir(path)
	return

#Mini preprocessing function
def preprocess(imageFile):
	image = cv2.imread(imageFile)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	height, width = image.shape[:2]
	#crop to 70%
	imCrop = image[int(0.15*height):int(0.85*height),int(0.15*width):int(0.85*width)]
	imResized=cv2.resize(imCrop, (256,256))
	image = cv2.equalizeHist(imResized)	
	return image


def getMoment(image,size):
	moment = cv2.HuMoments(cv2.moments(image)).flatten()
	return moment[:size]

def mfilter(moment):
	#moment[0]*=1e+03
	#moment[1]*=1e+06
	#moment[2]*=1e+10
	moment[0]=log10(moment[0])
	moment[1]=log10(moment[1])
	moment[2]=log10(moment[2])

#Load the initial clusters (10)
f5 = h5py.File("ClusterFile.hdf5", "r")
clusters = np.array(f5.get('clusters'))

#clusters = np.delete(clusters,7,axis =1)

print "Clusters loaded. Dimension:",clusters.shape

#folder for dataset images
input_path = '/home/shubham/Desktop/project/Dataset/ManipurEarthquake'
output_path = 'mout'
critial_match = 15 #30 percent

#scan the input files
onlyfiles = [ f for f in listdir(input_path) if isfile(join(input_path,f)) ]



#Create a set for each cluster
sets = [set() for _ in xrange(clusters.shape[0])]
#Intialize the minhash data structures
comparator = Comparator()

import progressbar
bar = progressbar.ProgressBar(maxval=len(onlyfiles), \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])


bar.start()
i = 0
for f in onlyfiles:
	img = preprocess(join(input_path,f))
	feature = getMoment(img,clusters.shape[1])
	mfilter(feature)
	#print feature
	#Find the two nearest clusters
	dists = euclidean_distances(feature.reshape(1, -1),clusters)
	arr = dists.argsort()[-2:][::-1]
	cluster1 = arr[0][0]
	cluster2 = arr[0][1]
	#print cluster1,",",cluster2
	
	localbuckets = sets[cluster1]|sets[cluster2]
	sign = comparator.createSign(img)
	
	#If uninon of nearest clusters are not empty
	if localbuckets:		
		matched = False
		for lb in localbuckets:
			match = comparator.compareSignature(lb.getSign(),sign)
			if match>=critial_match:
				#print "match found"
				lb.addSign(f,sign)
				matched = True
				break
				
		if not matched:
			#print "creating new bucket"
			b = Bucket(f,sign)
			sets[cluster1].add(b)
			sets[cluster2].add(b)			
				
	else:
		#No local bucket
		b = Bucket(f,sign)
		sets[cluster1].add(b)
		sets[cluster2].add(b)
		
	bar.update(i)
	i+=1

bar.finish()

makeDir(output_path)
makeDir(join(output_path,"others"))
allbuckets = set.union(*sets)

for b in allbuckets:
	print "Bucket #"+str(b.bid)+" size:"+str(b.size)
	print b.image_list
	
	if(b.size>1):
		makeDir(join(output_path,"bucket"+str(b.bid)))
		for img in b.image_list:
			copyfile(join(input_path,img),join(output_path,"bucket"+str(b.bid),img))
	else:
		copyfile(join(input_path,b.image_list[0]),join(output_path,"others",b.image_list[0]))	
