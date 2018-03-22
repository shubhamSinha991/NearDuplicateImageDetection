import numpy as np

class Bucket:
	'Tuple of signature and image count'
	BUCKET_COUNT = 0
	size = 0
	signature = None
	bid = None 	#Bucket ID
	image_list = None
	
	def __init__(self,image_path,image_sign):
		self.signature = image_sign
		Bucket.BUCKET_COUNT+=1
		self.bid = Bucket.BUCKET_COUNT
		self.size = 1		
		self.image_list = [image_path]
		print "Bucket created with ID "+str(self.bid)
		
	def addSign(self,image_path,image_sign):
		#signature is updated as avg
		self.image_list.append(image_path)
		self.signature = self.size*self.signature + image_sign
		self.size+=1
		self.signature/=self.size
		self.signature = np.around(self.signature)		
			
	def getSign(self):
		return self.signature
	
	
