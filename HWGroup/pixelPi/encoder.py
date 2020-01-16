from bitstring import BitArray
import math
import Node

xpos_len = 4 # 4 bits -> 0-15
xpos_start = 0 # x starts at bit 0 in x+y bits
ypos_len = 4 # 4 bits -> 0-15
ypos_start = xpos_len # y starts at bit len(xpos in bits) in x+y bits
xy_len = xpos_len + ypos_len # total lengh of x+y bits
message_length = 20 * 8 # in bits
group_id_len = 4 # bits used for group id
group_size = 2^4 # currently 19

def encodeMessage(map):    
	''' Function to encode seat positions for sending via message_length BLE broadcasts
	Args:
	@map (Array of Tuples or Arrays): Format of tuples/arrays is [(int)id, (int)x, (int)y]

	Returns:
	@ (string): String of encoded ids with their coords
	'''
	sorted_map = sorted(map, key=lambda x: x[0])
	message_ba = BitArray('')
	
	for i in range(len(sorted_map)):
		message_ba.append(hex(sorted_map[i][0]>>4))
		message_ba.append(hex(sorted_map[i][0]&0b1111))
		message_ba.append(hex(sorted_map[i][1]))
		message_ba.append(hex(sorted_map[i][2]))

	return message_ba.tobytes().decode('cp437')
	
def decodeMessage(message):
	''' Function to decode seat positions for sending via message_length BLE broadcasts
	Args:
	@messages (string): Should be the full output from encodeMessage

	Returns:
	@map (array of tuples): format of tuples is ((int)id, (int)x, (int)y)
	'''
	seat_map = []
	message_bytes = BitArray(message.encode('cp437')).tobytes()
	for i in range(0, len(message_bytes),2):
		byte0 = message_bytes[i]
		byte1 = message_bytes[i+1]
		seat_map.append((int(byte0), int(byte1)&0b1111, int(byte1)>>4))
	return seat_map