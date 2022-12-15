from firebase_admin import credentials, initialize_app, storage
import time
import requests
import io

class BackendService:
    def __init__(self, database_url, credential, bucket_name) -> None:
        self.__database_url = database_url
        self.__credential = credentials.Certificate(credential)
        self.__bucket_name = bucket_name
        initialize_app(self.__credential)
        
        self.__bucket = storage.bucket(self.__bucket_name)
    
    def upload_image(self, name, image):
        # Upload image to firebase storage
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        image = img_byte_arr.getvalue()

        num = int(round(time.time() * 1000))
        local_time = time.ctime(time.time())
        new_name = name+"_"+str(local_time).replace(':', '_')+'.png'

        blob = self.__bucket.blob(new_name)
        blob.upload_from_string(image, content_type='image/png')
        blob.make_public()
        return {
            'name': new_name,
            'image_url': blob.public_url,
            'local_time': local_time,
            'face_id': num,
        }
    
    def save_to_database(self, name, image_url, local_time, face_id):
        # Save data to firebase realtime database
        data = {
            face_id: {
                'fullname': name,
                'url': image_url,
                'date': str(local_time)
            }
        }
        print('=======================')
        print('SAVE TO DATABASE')
        print(data)
        print('=======================')
        requests.post(self.__database_url + '/History/.json', json=data)