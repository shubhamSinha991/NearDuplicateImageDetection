import numpy as np
import h5py
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.cluster import KMeans
from os import listdir
from os.path import isfile, join
import cv2
from shutil import copyfile
import os,sys
import matplotlib.pyplot as plt

def preprocess(imageFile):
	image = cv2.imread(imageFile)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	height, width = image.shape[:2]
	#print height,"X",width
	#crop to 70%
	image = image[int(0.15*height):int(0.85*height),int(0.15*width):int(0.85*width)]
	image = cv2.equalizeHist(image)	
	return image


def getMoment(image,size):
	moment = cv2.HuMoments(cv2.moments(image)).flatten()
	return moment[:size]

def mfilter(moment):
	moment[0]*=1e+03
	moment[1]*=1e+06
	moment[2]*=1e+10
		
input_path = '/home/shubham/Desktop/project/vvdataset'
	
onlyfiles = [ f for f in listdir(input_path) if isfile(join(input_path,f)) ]	

X = None

i = 1
for f in onlyfiles:
	img = preprocess(join(input_path,f))
	mm = getMoment(img,3)
	#print i,". ",mm
	mfilter(mm)
	#print f
	#print i,". af: ",mm
	if X is None:
		X = mm
	else:
		X = np.vstack((X,mm))
	i+=1



print("clustering...")
result = KMeans(n_clusters=10,max_iter=500).fit(X)
print result.labels_

print np.bincount(result.labels_)
plt.hist(result.labels_,bins=[0,1,2,3,4,5,6,7,8,9])
plt.show()
ht, wid = result.cluster_centers_.shape[:2]
print ht,"X",wid

f5 = h5py.File("ClusterFile.hdf5", "w")
f5.create_dataset('clusters', data=result.cluster_centers_)
f5.close()
