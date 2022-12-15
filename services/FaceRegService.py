from numpy import asarray, expand_dims
from mtcnn.mtcnn import MTCNN
from PIL import Image
from os import listdir
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import LabelEncoder

class FaceRegService:
    def __init__(self, model, joblib):
        self.__face_netmodel = model
        self.__svm_model = joblib
        self.detector = MTCNN()
        self.faces = self.__init_faces(directory='image/train')
        self.in_encoder = Normalizer(norm='l2')
        self.out_encoder = self.__init_out_encoder()

    def predict(self, frame):
        screen, name, prob = self.__process_predict(frame)
        return {
            'screen': screen,
            'name': name,
            'prob': prob,
        }

    def __process_predict(self, frame):
        face_pixels = self.__extract_face(frame)

        face_pixel = self.__get_embedding(face_pixels)
        face_pixel = expand_dims(face_pixel, axis=0)

        face_pixel = self.in_encoder.transform(face_pixel)

        yhat_class = self.__svm_model.predict(face_pixel)

        yhat_prob = self.__svm_model.predict_proba(face_pixel)

        class_index = yhat_class[0]
        class_probability = yhat_prob[0, class_index] * 100

        if class_probability < 65:
            screen = "Stranger detected!"
            print(screen)
            return [screen, "Stranger", class_probability]
        
        predict_names = self.out_encoder.inverse_transform(yhat_class)
        print('Predicted: %s (%.3f)' % (predict_names[0], class_probability))
        screen = 'Hello %s' % predict_names[0]

        return [screen, predict_names[0], class_probability]
        


    def __extract_face(self, frame, required_size=(160, 160)):
        image = Image.fromarray(frame)
        image = image.convert('RGB')
        image_array = asarray(image)

        results = self.detector.detect_faces(image_array)
        if len(results) == 0:
            raise Exception("No face detected !")

        x1, y1, width, height = results[0]['box']

        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height

        face_array = image_array[y1:y2, x1:x2]

        face_image = Image.fromarray(face_array)
        face_image = face_image.resize(required_size)
        face_array = asarray(face_image)

        return face_array

    def __init_faces(self, directory):
        return [subdir for subdir in listdir(directory)]
    
    def __init_out_encoder(self):
        out_encoder = LabelEncoder()
        out_encoder.fit(self.faces)
        return out_encoder

    def __get_embedding(self, face_pixels):
        face_pixels = face_pixels.astype('float32')
        mean = face_pixels.mean()
        std = face_pixels.std()
        face_pixels = (face_pixels - mean) / std

        samples = expand_dims(face_pixels, axis=0)
        yhat = self.__face_netmodel.predict(samples)
        return yhat[0]
