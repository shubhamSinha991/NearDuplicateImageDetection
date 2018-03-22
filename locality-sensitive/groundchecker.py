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
	image = image[int(0.15*height):int(0.85*height),int(0.15*width):int(0.85*width)]
	image = cv2.equalizeHist(image)	
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
input_path = '/home/shubham/Desktop/project/GroundTruth'
output_path = 'mout'
critial_match = 15 #30 percent

onlydirs = [ f for f in listdir(input_path) if not isfile(join(input_path,f)) ]
for d in onlydirs:
	print d	
	#scan the input files
	onlyfiles = [ f for f in listdir(join(input_path,d)) if isfile(join(input_path,d,f)) ]
	#print join(input_path,d)
	
	for f in onlyfiles:
		img = preprocess(join(input_path,d,f))
		feature = getMoment(img,clusters.shape[1])
		mfilter(feature)
		#print feature
		#Find the two nearest clusters
		dists = euclidean_distances(feature.reshape(1, -1),clusters)
		arr = dists.argsort()[-2:][::-1]
		cluster1 = arr[0][0]
		cluster2 = arr[0][1]
		print "(",cluster1,",",cluster2,") ",f
	print "-------------------------------------------------------"
