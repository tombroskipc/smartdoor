from typing import Callable
from Adafruit_IO import Client, MQTTClient
from constant import *
from os import getenv

from services.AdafruitService import AdafruitService
from services.CaptureService import CaptureService
from services.FaceRegService import FaceRegService
from services.ModelService import ModelService

def setup_capture_service():
    print('SETUP CAPTURE')
    capture_service = CaptureService()
    print('DONE SETUP CAPTURE!')
    return capture_service

def setup_facereq_service():
    print('SETUP MODEL')
    model_service = ModelService(
        getenv('FACENET_MODEL_PATH'), 
        getenv('JOBJIB_PATH')
    )
    print('DONE SETUP MODEL!')

    print('SETUP FACE REQ')
    face_req = FaceRegService(model_service.facenet_model(), model_service.svm_model())
    print('DONE SETUP FACE REQ!')
    return face_req

def setup_adafruit_service(capture_service: CaptureService, face_req_service: FaceRegService):
    print('SETUP ADAFRUIT')
    aio = Client(getenv('AIO_USERNAME'), getenv('AIO_KEY'))
    client = MQTTClient(getenv('AIO_USERNAME'), getenv('AIO_KEY'))
    adafruit_service = AdafruitService(aio, client, {
        'capture_service': capture_service,
        'face_req_service': face_req_service
    })

    adafruit_service.subcribe_new_device(AIO_DOOR_BUTTON_FEED)
    adafruit_service.subcribe_new_device(AIO_THERMAL)
    adafruit_service.subcribe_new_device(AIO_CAPTURE_BUTTON_FEED)
    print('DONE SETUP ADAFRUIT!')
    return adafruit_service