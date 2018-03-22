import cv2
import numpy as np
6import h5py
from os import listdir
from os.path import isfile, join

dirname='/home/shubham/project/siftresults'

f5 = h5py.File("keypoints.hdf5", "w")

mypath='/home/shubham/project/vvdataset'
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

#for first image . descs can't be empty/zeros initially as the values will be appended
#calculating the first set of kp decriptors first and then appending to the array

img = cv2.imread( join(mypath,onlyfiles[0]) )
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
 
sift = cv2.xfeatures2d.SIFT_create()
(kp, descs) = sift.detectAndCompute(gray, None)

height, width = img.shape[:2]
img=np.zeros((height,width,3), np.uint8)
 
cv2.drawKeypoints(gray,kp,img,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
cv2.imwrite(join(dirname,'siftkp_0.jpg'),img)

print("# kps: {}, descriptors: {}".format(len(kp), descs.shape))

print descs

#for second image onwards. append decriptors to the descriptors of first
for n in range(1, len(onlyfiles)):

	img = cv2.imread( join(mypath,onlyfiles[n]) )
	gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
 
	sift = cv2.xfeatures2d.SIFT_create()
	(kp, descs1) = sift.detectAndCompute(gray, None)

	height, width = img.shape[:2]
	img=np.zeros((height,width,3), np.uint8)
 
	cv2.drawKeypoints(gray,kp,img,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 	
	filename = 'siftkp_%d.jpg'%(n,)

	cv2.imwrite(join(dirname,filename),img)

	print("# kps: {}, descriptors: {}".format(len(kp), descs1.shape))

	print descs1
	
	descs=np.vstack([descs,descs1])

print descs.shape

print descs	

f5.create_dataset('dataset_1', data=descs)

