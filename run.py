from Adafruit import Adafruit
from Adafruit_IO import Client, MQTTClient
from constant import *
from time import sleep
from FaceReg import FaceReg

def setup_adafruit():
    print('SETUP ADAFRUIT')
    aio = Client(AIO_USERNAME, AIO_KEY)
    client = MQTTClient(AIO_USERNAME, AIO_KEY)
    adafruit = Adafruit(aio, client)
    adafruit.subcribe_new_device(AIO_BUTTON_FEED)
    print('DONE!')
    return adafruit

def setup_facereq():
    print('SETUP FACE REQ')
    face_req = FaceReg(MODEL_PATH, JOB_LIB_PATH)
    print('DONE')
    return face_req


def main():
    face_req_client = setup_facereq()
    adafruit_client = setup_adafruit()
    
    print('FINISH SETUP')
    
    frame_path = face_req_client.get_frame()
    result = face_req_client.predict(frame_path)
    print(result)
    if (result['name'] != 'Stranger'):
        print('OPEN DOOR')
        adafruit_client.publish(AIO_BUTTON_FEED, OPEN_DOOR_VALUE)
        sleep(5)
        adafruit_client.publish(AIO_BUTTON_FEED, CLOSE_DOOR_VALUE)

if __name__ == '__main__':
    main()