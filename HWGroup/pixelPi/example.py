import BLE

device_type = 0

# Rx Messages
# def listen(UUID = "ABC4", maxNumMessages = 5)
if device_type == 0:
	message = BLE.listen()

#Tx Messages
# def broadcast_setup()
# def broadcast(data, UUID = "ABC4", Number_of_Broadcast_Cycles = 3, Time_Between_Transmissions = 15)
if device_type:
	message = "Hello!"
	broadcast_setup() # Only need to call this once after boot (or after using listen function)
	broadcast(message)
