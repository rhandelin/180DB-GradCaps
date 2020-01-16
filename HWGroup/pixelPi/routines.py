import board
import neopixel
import time
import math

def horizontal_scroll(pixels,i,coords,max_dim,gradient):
	i = coords[0] + i
	if i > max_dim[0]:
		i = i - max_dim[0]
	px = gradient[0]*(i)
	if px > 255:
		px = 255
	pixels.fill((px, 255-px, 0))

def vertical_scroll(pixels,i,coords,max_dim,gradient):
	i = coords[1] + i
	if i > max_dim[1]:
		i = i - max_dim[1]
	px = gradient[1]*(i)
	if px > 255:
		px = 255
	pixels.fill((px, 255-px, 0))

	


