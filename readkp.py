import cv2
import numpy as np
import h5py

f = h5py.File("keypoints.hdf5", "r")
f5 = h5py.File("vv.hdf5", "w")

data = f.get('dataset_1')
descs = np.array(data)

print descs.shape

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 5, 1.0)
ret,label,center=cv2.kmeans(descs,2000,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

print center.shape
print center

f5.create_dataset('dataset_1', data=center)
