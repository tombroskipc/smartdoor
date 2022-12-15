from keras.models import load_model
from joblib import dump, load
from os import getenv, listdir
# from os.path import isdir
# from numpy import asarray, expand_dims
# from PIL import Image

class ModelService:
    def __init__(self, model_input_path, joblib_output_path) -> None:
        self.__model_input_path = model_input_path
        self.__joblib_output_path = joblib_output_path
        # self.__train_folder_path = getenv('TRAIN_FOLDER_PATH')
        # self.__test_folder_path = getenv('TEST_FOLDER_PATH')


        # if getenv('NEED_TRAINING') == 'True':
        #     self.train()
        self.__svm_model = load(self.__joblib_output_path)
        self.__face_netmodel = load_model(filepath=self.__model_input_path, compile=False)
        # self.__svm_model = load(joblib_output_path)
        # self.__face_netmodel = load_model(filepath=model_input_path, compile=False)
    

    def svm_model(self):
        return self.__svm_model
    
    def facenet_model(self):
        return self.__face_netmodel

    # def train(self):
    #     facenet_model = load_model(filepath=self.__model_input_path)
    #     trainX, trainy = self.__load_dataset(self.__train_folder_path)


    # def __load_dataset(self, directory):
    #     x, y = list(), list()

    #     for subdir in listdir(directory):
    #         path = directory + subdir + '/'
    #         if not isdir(path):
    #             continue
    #         faces = self.__load_faces(path)
    #         labels = [subdir for _ in range(len(faces))]

    #         print('>loaded %d examples for class: %s' % (len(faces), subdir))

    #         x.extend(faces)
    #         y.extend(labels)
    
    #     return asarray(x), asarray(y)

    # def __load_faces(self, directory):
    #     return [
    #         self.__extract_face(directory + filename)
    #         for filename in listdir(directory)
    #     ]
    

    # def __extract_face(self, filename, required_size=(160, 160)):
    #     image = Image.open(filename)
    #     image = image.convert('RGB')
    #     image = asarray(image)

    #     results = self.detector.detect_faces(image)
    #     if len(results) == 0:
    #         raise Exception("No face detected !")

    #     x1, y1, width, height = results[0]['box']

    #     x1, y1 = abs(x1), abs(y1)
    #     x2, y2 = x1 + width, y1 + height

    #     face = image[y1:y2, x1:x2]

    #     image = Image.fromarray(face)
    #     image = image.resize(required_size)
    #     face_array = asarray(image)

    #     return face_array