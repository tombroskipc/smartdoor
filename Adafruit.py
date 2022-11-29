from typing import List
import  sys
from Adafruit_IO import Client, MQTTClient


class Adafruit:
    __client: MQTTClient
    __aio: Client
    feed_list: List[str]
    def __init__(self, aio: Client, client: MQTTClient) -> None:
        self.__aio = aio
        self.__client = client
        self.__client.on_connect = self.__connected
        self.__client.on_disconnect = self.__disconnected
        self.__client.on_message = self.__message
        self.__client.on_subscribe = self.__subscribe

        self.__client.connect()
        self.__client.loop_background()

        self.feed_list = []

    def __connected(self, client):
        self.log_data('CONNECT SUCCESSFULLY')
    
    def __subscribe(self, client , userdata , mid , granted_qos):
        self.log_data('SUBCRIBE SUCCESSFULLY')

    def __disconnected(self, client):
        self.log_data('DISCONNECT SUCCESSFULLY')
        sys.exit(1)

    def __message(self, client: MQTTClient , feed_id, payload):
        self.log_data('Recrive data: ', {
            'feed': feed_id,
            'payload': payload,
        })
    
    def subcribe_new_device(self, feed_id: str):
        self.__client.subscribe(feed_id)
        self.feed_list.append(feed_id)

    def publish(self, feed_id, value):
        self.__client.publish(feed_id, value)
    
    def log_data(self, topic, log='NOTHING'):
        print('=======================')
        print(topic)
        if log != 'NOTHING':
            print(log)
        print('=======================')
