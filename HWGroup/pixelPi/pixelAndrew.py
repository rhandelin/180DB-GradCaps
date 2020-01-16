#import board
#import neopixel
import BLE
from PIL import Image
import os
import numpy as np
from BLE import broadcast_setup, broadcast, listen

#When receives a radio message, save to file
#Then attempt to load the file
BLE_broadcast_setup()
device_type = 0 #This is a receiver

def load_my_role(file = 'role.txt'):
	f = open(file,"r")
	msg = f.read()
	f.close()
	return np.uint8(int(msg))

def load_pixel_role(x, y, img = 'img.jpeg'):
	im = Image.open(img)
	pix = im.load()
	this_pix = pix[x, y]
	return this_pix[0:3]

def decodemessage(string_input, my_role):
	_bytes = bytearray(string_input)
	for index in range(0, len(_bytes), 4):
		msg = _bytes[index:index+4]
		row = np.uint8(msg[0])
		col = np.uint8(msg[1])
		role_id = np.uint8(msg[2])
		mode = np.uint8(msg[3])

		if role_id == my_role:
			return [row, col, role_id, mode] #return what my message is

def loop_listen():
	#message = ""
	#while(message != ""):
	#	message = BLE_listen()
	#return message
	message = listen()
	return message

def load_file(file = "save.txt"):
	if os.path.exists("myfile.dat"):
		f = open(file,"r")
		msg = f.read()
		f.close()
		return msg
	else:
		return None

def save_file(msg, file = "save.txt"):
	f = open(file, "w")
	f.write(msg, file)
	return True

if device_type == 0:
	message = load_file()
	if message == None:
		message = loop_listen()
	save_file(message)

	list_decoded = decodemessage(message, load_my_role)
	pixel_tuple = load_pixel_role(list_decoded[0], list_decoded[1], img = 'img' + list_decoded[3] + '.jpeg')

	print(pixel_tuple)
	#pixels = neopixel.NeoPixel(board.D18, 12)
	#pixels.fill(pixel_tuple)