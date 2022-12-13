from recognize import load_model, load, predict
import cv2
from time import time
class FaceReg:
    frame_path: str
    camera: cv2.VideoCapture
    def __init__(self, model_path: str, joblib_path: str):
        self.__face_netmodel = load_model(filepath=model_path, compile=False)
        self.__svm_model = load(joblib_path)
        self.camera = cv2.VideoCapture(0)
        self.frame_path = 'capture/'

    def save_frame_asap(self, frame):
        img_name = str(int(time()))
        path = self.frame_path + img_name + '.png'
        cv2.imwrite(path, frame)
        return path

    def get_frame(self):
        ret, frame = self.camera.read()
        if not ret:
            raise "failed to grab frame"
        
        return self.save_frame_asap(frame)

    def predict(self, frame_path):
        screen, name, prob = predict(frame_path, self.__svm_model, self.__face_netmodel)
        return {
            'screen': screen,
            'name': name,
            'prob': prob,
        }
