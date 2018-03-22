import cv2
import numpy as np
from math import pow, sqrt
import time
from sklearn.metrics.pairwise import euclidean_distances


current_milli_time = lambda: int(round(time.time() * 1000))

def createSignature(filename,center,a,b,c) :
	detect_time = current_milli_time()
	
	print "\nreading file "+filename
	ti = cv2.imread(filename)
	gray= cv2.cvtColor(ti,cv2.COLOR_BGR2GRAY)
	sift = cv2.xfeatures2d.SIFT_create(100)		#maximum 100 keypoints
	(kp_ti, descs_ti) = sift.detectAndCompute(gray, None)

	total_kp=descs_ti.shape[0]
	temp=np.zeros(total_kp)
	temp1=np.zeros(total_kp)
	sig_ti=np.zeros(50)	
	
	
	pairwise_time = current_milli_time()
	dists = euclidean_distances(descs_ti,center)	
	
	for i in range(0,dists.shape[0]):
		temp[i] = dists[i].argmin()	#min_index
		#print str(i)+". "+str(temp[i])
			
	
	hash_time = current_milli_time()
	
	for m in range(0,50):#for 50 hash functions, 50 elements in signature
		for n in range(0,total_kp):
			temp1[n]=((a[m]*temp[n])+b[m])%c	#apply hash function on the array of the indexes
		#print(temp1.min())
		sig_ti[m]=temp1.min()	#find minimum. this is the ith element of signature
	
	
	#time measurements
	end_time = current_milli_time()
	print "signature created in "+str((end_time-detect_time))+" ms  ( detection:"+\
		str(pairwise_time - detect_time) + "ms  pairwise:"+str(hash_time-pairwise_time)+"ms  hashing:"+\
		str(end_time-hash_time)+"ms )"
		
		
	#print sig_ti
	return sig_ti
	
	
def compareSignature(sign_a,sign_b):
	if(sign_a.shape[0]!=sign_b.shape[0]):
		print "sign dimensions do not match"
		return
	match = 0
	for i in range(0,sign_a.shape[0]):
		if(sign_a[i]==sign_b[i]) :
			match += 1
	return match

