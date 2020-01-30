import numpy as np

class Text2Vec(object):

	def __init__(self,height=5,width=3):
		self.basis = np.zeros((height,width))
		self.width = width
		self.height = height

		self.middle = [int(height/2)+1,int(width/2)+1]

	def __str__(self):
		return str(self.basis)

	def reset(self):
		self.basis = np.zeros((self.height,self.width))

	def diagonal(self, start, slope, direction,color=1):
		print(start)
		height = start[0]
		width = start[1]
		if direction > 0:
			while(height >= 0 and width < self.width):
				print(height, width)
				self.basis[height,width] = color
				height -= slope[0]
				width += slope[1]
		else:
			while(height < self.height and width < self.width):
				self.basis[height,width] = color
				height += slope[0]
				width += slope[1]

	def vertical(self,start,direction,color=1):
		height = start[0]
		width = start[1]
		if direction > 0:
			while(height < self.height and width < self.width):
				self.basis[height,width] = color
				height += 1
		else:
			while(height > 0):
				self.basis[height,width] = color
				height += 1

	def horizontal(self,start,direction,color=1):
		height = start[0]
		width = start[1]
		if direction > 0:
			while(width < self.width):
				self.basis[height,width] = color
				width += 1
		else:
			while(height > 0):
				self.basis[height,width] = color
				width -= 1


	def A(self):
		self.reset()
		self.diagonal((self.middle[0]-1,0),(2,1),1)
		self.diagonal((0,self.middle[1]),(2,1),-1)
		self.vertical((self.middle[0],0),1)
		self.vertical((self.middle[0],self.width-1),1)
		self.horizontal((self.middle[0],0),1)

text = Text2Vec(11,7)

print(text.middle)

text.A()

print(text)