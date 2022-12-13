import  sys
from Adafruit_IO import Client, Data, MQTTClient
import random, time

AIO_FEED_ID = "thermal"
AIO_USERNAME='tombroskipc'
AIO_KEY='aio_KmOV92TwDW6iz12jj0w2d2FHshkE'

def connected(client):
    print("Ket noi thanh cong...")
    client.subscribe(AIO_FEED_ID)

def  subscribe(client , userdata , mid , granted_qos):
    print("Subcribe thanh cong...")

def  disconnected(client):
    print("Ngat ket noi...")
    sys.exit (1)

def  message(client: MQTTClient , feed_id , payload):
    print("Nhan du lieu: " + payload)
    client.publish(AIO_FEED_ID, 1)

aio = Client(AIO_USERNAME, AIO_KEY)
client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

client.connect()
client.loop_background()

value = 80
print ("Update :", value )
client.publish(AIO_FEED_ID, value)