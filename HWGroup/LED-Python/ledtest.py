import board
import neopixel
import time
import math

pixels = neopixel.NeoPixel(board.D18, 12)
pixels.fill((255, 255, 255))

def horizontal_scroll(i,coords,max_dim,gradient):
	i = coords[0] + i
	if i > max_dim[0]:
		i = i - max_dim[0]
	px = gradient[0]*(i)
	if px > 255:
		px = 255
	pixels.fill((px, 255-px, 0))

def vertical_scroll(i,coords,max_dim,gradient):
	i = coords[1] + i
	if i > max_dim[1]:
		i = i - max_dim[1]
	px = gradient[1]*(i)
	if px > 255:
		px = 255
	pixels.fill((px, 255-px, 0))

max_dim = (12,12)
coords = (3,2)
gradient = (math.ceil(255/(max_dim[0]-1)), math.ceil(255/(max_dim[1]-1)))

for i in range(2):
	for i in range(12):
		horizontal_scroll(i, coords, max_dim, gradient)
		time.sleep(0.5)

for i in range(2):
	for i in range(12):
		vertical_scroll(i, coords, max_dim, gradient)
		time.sleep(0.5)
