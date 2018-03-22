import cv2
import numpy as np
import h5py
from os import listdir
from os.path import isfile, join
from math import pow, sqrt
from random import randint

a=np.zeros(50)
b=np.zeros(50)


for i in range(0,50):
	a[i]=randint(1,2000)
	b[i]=randint(1,2000)
c=2003

f5 = h5py.File("vv.hdf5", "r")
data = f5.get('dataset_1')
center = np.array(data)

ti = cv2.imread('flower.jpg')
gray= cv2.cvtColor(ti,cv2.COLOR_BGR2GRAY)
 
sift = cv2.xfeatures2d.SIFT_create()
(kp_ti, descs_ti) = sift.detectAndCompute(gray, None)

total_kp=descs_ti.shape[0]
temp=np.zeros(total_kp)
temp1=np.zeros(total_kp)
sig_ti=np.zeros(50)

for i in range(0,total_kp):#for each keypoint 
	min_index=0
	
	for j in range(0,center.shape[0]):#to find index of center with which min distance
		sqsum=0
		for k in range(0,128):#to find distance of 128 dimensions
			sqsum=sqsum+pow((descs_ti[i,k]-center[j,k]),2)	
		dist=sqrt(sqsum)
		if j==0:
			min_dist=dist
		elif min_dist>dist:
			min_dist=dist
			min_index=j

	temp[i]=min_index

for m in range(0,50):#for 50 hash functions, 50 elements in signature
	for n in range(0,total_kp):
		temp1[n]=((a[m]*temp[n])+b[m])%c#apply hash function on the array of the indexes
	print(temp1.min())
	sig_ti[m]=temp1.min()#find minimum. this is the ith element of signature

print sig_ti
