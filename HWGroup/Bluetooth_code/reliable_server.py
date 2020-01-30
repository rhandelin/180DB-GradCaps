from bluetooth import *
from gpiozero import PWMLED
import time

led_1 = PWMLED(12)
led_2 = PWMLED(16)
led_3 = PWMLED(20)
led_4 = PWMLED(21)

def receiveMessages(uuid = "aaf39d29-7d6d-437d-973b-fba39e49d4ee"):

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
	
	try:
			while True:
				for x in range(len(led1_data)):
					led1 = led1_data[x]
					led2 = led2_data[x]
					led3 = led3_data[x]
					led4 = led4_data[x]
					data = client_sock.recv(1024)
					
					if led1 == '1':
						led_1.on()
					else:
						led_1.off()
			
					if led2 == '1':
						led_2.on()
					else:
						led_2.off()
			
					if led3 == '1':
						led_3.on()
					else:
						led_3.off()
			
					if led4 == '1':
						led_4.on()
					else:
						led_4.off()

					if len(data) == 0: break
					
	except IOError:
			pass

	print("disconnected")
	
	client_sock.close()
	server_sock.close()
	
	print("all done")
	
receiveMessages()
