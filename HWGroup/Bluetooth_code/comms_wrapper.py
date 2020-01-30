from bluetooth import *
from gpiozero import PWMLED
import time
import BLE

#An implementation of BLE of "announcements". The user can encode bytes any way he wants to, he just needs to decode.
#All "listeners" will receive the same message on their radios, but software processing can filter messages.
#EG a potential user could send a list encoded in bytes, with the first number indicating the identifier of the listener.

 #TODO: If you want to use the process_command function, you should have the following:
 #A dictionary that has a mapping of keys, values of: (str byte sequence), (str function_name in this class)
 #You should initialize this when you use this wrapper! This simply implements multiple callbacks that you could do!

class PythonBLE(object):
	def __init__(self, device_type = 0):
		#0 for receive, 1 for transmit
		broadcast_setup() # Only need to call this once after boot (or after using listen function)
		self.device_type = self.device_type

# Rx Messages
	def receiveMessages():
		if self.device_type == 0:
			msg = BLE.listen()
			#This is blocking, won't return until BLE gets something or times out.

	#Tx Messages
	# def broadcast_setup()
	# def broadcast(data, UUID = "ABC4", Number_of_Broadcast_Cycles = 3, Time_Between_Transmissions = 15)

	def transmit(msg):
		if device_type:
			broadcast(msg)

class PythonIR(object):
	#myIR = PythonIR({'16582903':'function_callback'})
	def __init__(self, recv_commands_dict, ir_pin = 16):

		irPin = ir_pin
		ir = IRModule.IRRemote(callback='DECODE')
		# using 'DECODE' option for callback will print out
		# the IR code received in hexadecimal
		# this can used to get the codes for whichever NEC
		# compatable remote you are using

		# set up GPIO options and set callback function required
		# by the IR remote module (ir.pWidth)        
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)      # uses numbering outside circles
		GPIO.setup(irPin,GPIO.IN)   # set irPin to input
		GPIO.add_event_detect(irPin,GPIO.BOTH,callback=ir.pWidth)

		ir.set_verbose(False) # verbose option prints outs high and low width durations (ms)


	def remote_callback(code):
		#Legacy. You can use the code number and use this function as a callback.
		if code == 16582903:
			print('Pressed: 1')
			pixels.fill((255,0,0))
		elif code == 16615543:
			print('Pressed: 2')
			pixels.fill((0,255,0))
		elif code == 16599223:
			print('Pressed: 3')
			pixels.fill((0,0,255))
		elif code == 16591063:
			print('Pressed: 4')
		elif code == 16623703:
			print('Pressed: 5')
		elif code == 16607383:
			print('Pressed: 6')
		elif code == 16586983:
			print('Pressed: 7')
		elif code == 16619623:
			print('Pressed: 8')
		elif code == 16603303:
			print('Pressed: 9')
		elif code == 16593103:
			print('Pressed: 0')
			pixels.fill((255,255,255))
		elif code == 16605343:
			print('Pressed: Stop')
			pixels.fill((0,0,0))
		else:
			if code != -1:
				print(code)# unknown code
		return

	def start_listening_legacy(self):    
		try:
			#time.sleep(5)

			# turn off verbose option and change callback function
			# to the function created above - remote_callback()
			print('Ready')
			ir.set_verbose(False)
			ir.set_callback(remote_callback)

			# This is where you could do other stuff
			# Blink a light, turn a motor, run a webserver
			# count sheep or mine bitcoin

		except:
			print('Removing callback and cleaning up GPIO')
			ir.remove_callback()
			GPIO.cleanup(irPin)

	def start_listening(self):
		callback = lambda a: process_command(process_data(a))
		try:
			ir.set_verbose(False)
			ir.set_callback(callback)

		except:
			print('Removing callback and cleaning up GPIO')
			ir.remove_callback()
			GPIO.cleanup(irPin)


	def process_data(self, data):
		#Feed this output to process_command to call some function within this class
		try:
			self.recv_commands_dict[str(data)] 
		except:
			print('The received IR command was invalid')
			pass
		return self.recv_commands_dict[str(data)] 

	def process_command(self, cmd):
		#Command is the function you want to run within this class.
		result = getattr(self, str(cmd))()
		return result
	 
#mypythonIR = PythonIR({'123' : start_game})


#Implementation of sending messages of bluetooth. You need to know the UUID of the targetbluetoothmac, however. (UUID)
class PythonBluetooth(object):
	def __init__(self, recv_commands_dict):
		self.recv_commands_dict = recv_commands_dict


	def sendMessageTo(self, targetBluetoothMacAddress, msg):
		port = 1
		sock=BluetoothSocket( bluetooth.RFCOMM )
		sock.connect((targetBluetoothMacAddress, port))
		sock.send(str(msg))
		sock.close()
		
	def sendDoneMessage(self, targetBluetoothMacAddress):
		#This is an implementation of an ACK
		port = 1
		sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
		sock.connect((targetBluetoothMacAddress, port))
		sock.send("done!")
		sock.close()
		
	def lookUpNearbyBluetoothDevices(self, verbose = False):
		nearby_devices = bluetooth.discover_devices()
		if verbose == True:
			for bdaddr in nearby_devices:
				print (str(bluetooth.lookup_name( bdaddr )) + " [" + str(bdaddr) + "]")
		return nearby_devices

	def connect_to_server(self, address,uuid):
		addr = address
		
		# search for the SampleServer service
		uuid = server_num
		service_matches = find_service( uuid = uuid, address = addr )

		if len(service_matches) == 0:
			print("couldn't find the SampleServer service =(")
			sys.exit(0)

		first_match = service_matches[0]
		port = first_match["port"]
		name = first_match["name"]
		host = first_match["host"]

		print("connecting to \"%s\" on %s" % (name, host))

		# Create the client socket
		sock=BluetoothSocket( RFCOMM )
		sock.connect((host, port))

		#print("connected.	type stuff")
		return sock, service_matches

		#This looks like a server thing, but could be done on a rbp as well?
		#TODO: Test when this breaks

	def receiveMessages(uuid):

		server_sock=BluetoothSocket( RFCOMM )
		server_sock.bind(("",PORT_ANY))
		server_sock.listen(1)

		port = server_sock.getsockname()[1]

		advertise_service( server_sock, "SampleServer",
						 service_id = uuid,
						 service_classes = [ uuid, SERIAL_PORT_CLASS ],
						 profiles = [ SERIAL_PORT_PROFILE ], 
							)
						 
		print("Waiting for connection on RFCOMM channel %d" % port)

		client_sock, client_info = server_sock.accept()
		print("Accepted connection from ", client_info)

		data = client_sock.recv(1024)
		print("received [%s]" % data)


		client_sock.close()
		server_sock.close()
		return data

	def process_data(self, data):
		#Feed this output to process_command to call some function within this class
		return self.recv_commands_dict[str(data)] 

	def process_command(self, cmd):
		#Command is the function you want to run within this class.
		result = getattr(self, str(cmd))()
		return result

