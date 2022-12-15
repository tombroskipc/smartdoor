from typing import List, Callable
import sys
from Adafruit_IO import Client, MQTTClient
from constant import *
from time import sleep
from PIL import Image
from json import dumps
class AdafruitService:
    __client: MQTTClient
    __aio: Client
    feed_list: List[str]

    def __init__(self, aio: Client, client: MQTTClient, services) -> None:
        self.__services = services
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

    def __subscribe(self, client, userdata, mid, granted_qos):
        self.log_data('SUBCRIBE SUCCESSFULLY')

    def __disconnected(self, client):
        self.log_data('DISCONNECT SUCCESSFULLY')
        sys.exit(1)

    def __message(self, client: MQTTClient, feed_id, payload):
        self.log_data('Recrive data: ', {
            'feed': feed_id,
            'payload': payload,
        })

        if feed_id == AIO_THERMAL and int(payload) > 70:
            print('ALTER TEMPERATURE TOO HIGH, AUTO OPEN DOOR')
            self.publish(AIO_DOOR_BUTTON_FEED, 1)
        elif feed_id == AIO_CAPTURE_BUTTON_FEED:
            self.__trigger()

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


    def __trigger(self):
        print('CAPTURE BUTTON PRESSED')
        try:
            frame = self.__services['capture_service'].get_frame()
            copy_frame = frame.copy()
            result = self.__services['face_req_service'].predict(frame)
            copy_image = Image.fromarray(copy_frame)
            copy_image = copy_image.convert('RGB')

            print(result)

            if (result['name'] != 'Stranger'):
                print('OPEN DOOR')
                self.publish(
                    AIO_DOOR_BUTTON_FEED,
                    OPEN_DOOR_VALUE
                )

                sleep(DOOR_WAIT_TIME)

                self.publish(
                    AIO_DOOR_BUTTON_FEED,
                    CLOSE_DOOR_VALUE
                )

            backend_data = self.__services['backend_service'].upload_image(
                result['name'],
                copy_image
            )
            self.log_data('BACKEND DATA', dumps(backend_data, indent=4))
            self.__services['backend_service'].save_to_database(
                backend_data['name'],
                backend_data['image_url'],
                backend_data['local_time'],
                backend_data['face_id']
            )
        except Exception as e:
            if str(e) == 'No face detected':
                print('NO FACE DETECTED, DO NOTHING')
            else:
                print(e)