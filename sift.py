import cv2
import numpy as np
import h5py

f = h5py.File("keypoints.hdf5", "w")


img = cv2.imread('flower.jpg')
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
 
sift = cv2.xfeatures2d.SIFT_create()
(kp, descs) = sift.detectAndCompute(gray, None)

height, width = img.shape[:2]
img=np.zeros((height,width,3), np.uint8)
 
cv2.drawKeypoints(gray,kp,img,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
cv2.imwrite('sift_keypoints.jpg',img)

print("# kps: {}, descriptors: {}".format(len(kp), descs.shape))

print descs

f.create_dataset('dataset_1', data=descs)

