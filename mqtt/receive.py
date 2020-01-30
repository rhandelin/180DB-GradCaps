import time
import board
import neopixel
import paho.mqtt.client as mqtt

pixel_pin = board.D18
num_pixels = 12
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)
f = open("/boot/id.txt",'r')
id=int(f.readline())


pixels.fill((0,0,0))
pixels.show()

MQTT_SERVER = "192.168.0.100"
MQTT_PATH = "test_channel"

# The callback for when the client receives a CONNACK response from the serv$
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    print(msg.payload)
    if msg.payload == "R":
        pixels.fill((255,0,0))
        pixels.show()
    elif msg.payload == "G":
        pixels.fill((0,255,0))
        pixels.show()
    elif msg.payload == "B":
        pixels.fill((0,0,255))
        pixels.show()
    elif msg.payload == "W":
        pixels.fill((255,255,255))
        pixels.show()
    elif msg.payload == "C":
        pixels.fill((0,0,0))
        pixels.show()
    elif msg.payload == "cmd1":
        print(id*5)
        time.sleep(0.5*id)
        pixels.fill((255,255,255))
        pixels.show()
        time.sleep(0.5)
        pixels.fill((0,0,0))
        pixels.show()

# more callbacks, etc
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()


