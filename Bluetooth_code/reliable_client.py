from bluetooth import *
from gpiozero import PWMLED
import time

led_1 = PWMLED(12)
led_2 = PWMLED(16)
led_3 = PWMLED(20)
led_4 = PWMLED(21)

def receiveMessages():
  
  
  led1_data = open("pixel_data_hat1.txt","r").read()
  led2_data = open("pixel_data_hat2.txt","r").read()
  led3_data = open("pixel_data_hat3.txt","r").read()
  led4_data = open("pixel_data_hat4.txt","r").read()
  
  data_length = len(led1_data)

  slave_1_sock = connect_to_server("B8:27:EB:88:3F:16",0)
  
  print("I connected to a slave")
  
  slave_2_sock = connect_to_server("B8:27:EB:91:65:E9",2)
  
  print("I connectect to another slave")
  
  slave_3_sock = connect_to_server("B8:27:EB:51:82:8A",1)
  
  print("I connected to the final slave")
  
  
  for x in range(data_length):
    slave_1_sock.send("kill")
    slave_2_sock.send("me")
    slave_3_sock.send("now")
    
    led1 = led1_data[x]
    led2 = led2_data[x]
    led3 = led3_data[x]
    led4 = led4_data[x]
    time.sleep(0.075)
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
    
    time.sleep(0.8)
    
  print("done sending messages")
  slave_1_sock.send("")
  slave_2_sock.send("")
  slave_3_sock.send("")
  print("Goodbye")
  
  slave_1_sock.close()
  slave_2_sock.close()
  slave_3_sock.close()
  server_sock.close()
  client_sock.close()
  

  
def sendMessageTo(targetBluetoothMacAddress):
  port = 1
  sock=BluetoothSocket( bluetooth.RFCOMM )
  sock.connect((targetBluetoothMacAddress, port))
  sock.send("hello!!")
  sock.close()
  
def sendDoneMessage(targetBluetoothMacAddress):
  #This is an implementation of an ACK
  port = 1
  sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  sock.connect((targetBluetoothMacAddress, port))
  sock.send("done!")
  sock.close()
  
def lookUpNearbyBluetoothDevices(verbose = False):
  nearby_devices = bluetooth.discover_devices()
  if verbose == True:
    for bdaddr in nearby_devices:
      print (str(bluetooth.lookup_name( bdaddr )) + " [" + str(bdaddr) + "]")
  return nearby_devices

def connect_to_server(address,uuid):
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

  print("connected.  type stuff")
  return sock, service_matches
  
receiveMessages()   
#sendMessageTo("B8:27:EB:88:3F:16") 
