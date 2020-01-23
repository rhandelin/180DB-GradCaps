import board
import neopixel
import time
import math

class Display(object):

	def __init__(self):
		self.pixels = neopixel.NeoPixel(board.D18, 12)
        self.colors = []
        for i in range(12):
            self.colors.append((0,0,0))

    def show(self):
        for i in range(12):
            self.pixels[i] = self.colors[i]
        self.pixels.show()

    def displayall(self,R,G,B):
        self.all(R,G,B)
        self.show()

    def pixel(self,ID,R,G,B):
        ID = int(ID)
        if ID < 0 or ID > 12:
            print("ERROR (Display.pixel): Incorrect ID Value")
            exit(1)
        self.colors[i] = (R,G,B)

    def corner(self, ID):
        # Valid ID inputs:
        # "F" or 0 : Front Corner
        # "B" or 1 : Back Corner
        # "R" or 2 : Right Corner
        # "L" or 3 : Left Corner

        if ID == "F" or ID == 0:
            self.colors[5] = (R,G,B)
            self.colors[6] = (R,G,B)
            self.colors[7] = (R,G,B)
        elif ID == "B" or ID == 1:
            self.colors[1] = (R,G,B)
            self.colors[0] = (R,G,B)
            self.colors[11] = (R,G,B)
        elif ID == "R" or ID == 2:
            self.colors[8] = (R,G,B)
            self.colors[9] = (R,G,B)
            self.colors[10] = (R,G,B)
        elif ID == "L" or ID == 3:
            self.colors[2] = (R,G,B)
            self.colors[3] = (R,G,B)
            self.colors[4] = (R,G,B)
        else:
            print("ERROR (Display.segment): Incorrect ID Value")
            exit(1)

	def segment(self,ID,R,G,B):
		# Valid ID inputs:
		# "FR" or 0 : Front_Right Segment
		# "FL" or 1 : Front_Left Segment
		# "BL" or 2 : Back_Left Segment
		# "BR" or 3 : Back_Right Segment

		if ID == "FR" or ID == 0:
			self.colors[7] = (R,G,B)
            self.colors[8] = (R,G,B)
		elif ID == "FL" or ID == 1:
			self.colors[4] = (R,G,B)
            self.colors[5] = (R,G,B)
		elif ID == "BL" or ID == 2:
			self.colors[1] = (R,G,B)
            self.colors[2] = (R,G,B)
		elif ID == "BR" or ID == 3:
			self.colors[10] = (R,G,B)
            self.colors[11] = (R,G,B)
		else:
			print("ERROR (Display.segment): Incorrect ID Value")
			exit(1)

    def all(self,R,G,B):
        for i in range(12):
            self.colors[i] = (R,G,B)
