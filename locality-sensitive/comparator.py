import numpy as np
import h5py
from siglib import createSignature
from os import listdir
from os.path import isfile, join
from random import randint

class Comparator:
	'Module initialized with a,b,c and dataset to compare'
	a = b = c = None
	center = None
	
	def __init__(self):
		self.a=np.zeros(50)
		self.b=np.zeros(50)

		for i in range(0,50):
			self.a[i]=randint(1,2000)
			self.b[i]=randint(1,2000)
		self.c=2003

		f5 = h5py.File("vv.hdf5", "r")
		data = f5.get('dataset_1')
		self.center = np.array(data)
		print "Module initialized"
	
	def createSign(self,image):
		return createSignature(image,self.center,self.a,self.b,self.c)
		
	def compare(self,image_a,image_b):
		sign_a = self.createSign(image_a)
		sign_b = self.createSign(image_b)
		return self.compareSignature(sign_a,sign_b)
		
	def compare(self,image_a,sign_b):
		return self.compareSignature(self.createSign(image_a),sign_b)
		
	def compareSignature(self,sign_a,sign_b):
		if(sign_a.shape[0]!=sign_b.shape[0]):
			print "sign dimensions do not match"
			return
		match = 0
		for i in range(0,sign_a.shape[0]):
			if(sign_a[i]==sign_b[i]) :
				match += 1
		return match	
	

