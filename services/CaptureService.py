from recognize import load_model, load, predict
import cv2
from time import time
class CaptureService:
    frame_path: str
    camera: cv2.VideoCapture
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.frame_path = 'capture/'

    # def save_frame_asap(self, frame):
    #     img_name = str(int(time()))
    #     path = self.frame_path + img_name + '.png'
    #     cv2.imwrite(path, frame)
    #     return path

    def get_frame(self):
        ret, frame = self.camera.read()
        if not ret:
            raise "failed to grab frame"
        
        return frame