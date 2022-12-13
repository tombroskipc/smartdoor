import firebase_admin
from firebase_admin.credentials import Certificate
from firebase_admin import auth as Auth
import traceback
import requests as RQ
import json
CRED_PATH = "credentials/service.json"

cred = Certificate("./credentials/service.json")
app = firebase_admin.initialize_app(cred)

REST_URL = 'https://identitytoolkit.googleapis.com/v1/accounts'
API_KEY = 'AIzaSyBbBh6L1VFH9x-lrUJ0NKYR9t1YMQY-oYc'

class REST:

    @staticmethod
    def build_url(option, query, base=REST_URL):
        queries = []
        for key in query:
            queries.append(f'{key}={query[key]}')
        query_str = '&'.join(queries)
        url = base + ':' + option + '?' + query_str
        return url

    @staticmethod
    def sign_in(email, password):
        url = REST.build_url('signInWithPassword', {
            'key': API_KEY
        })

        data = {
            'email': email,
            'password': password
        }

        return RQ.post(url, data).json()
        

class SDK:
    @staticmethod
    def sign_up(**kwargs):
        try:
            return Auth.create_user(**kwargs)
        except Exception as error:
            print(error)
            print(traceback.format_exc())
            
    @staticmethod
    def sign_in(**kwargs):
        try:
            return REST.sign_in(kwargs['email'], kwargs['password'])
        except Exception as error:
            print(error)
            print(traceback.format_exc())
            
    @staticmethod
    def edit_profile(**kwargs):
        try:
            pass
        except Exception as error:
            print(error)
            print(traceback.format_exc())
        

def sign_up():
    payload = {
        'display_name': 'Na',
        'email': 'nhatanh@gmail.com',
        'email_verified': False,
        'phone_number': '+84 923456789',
        'password': '123456789',
    }
    res = SDK.sign_up(**payload)
    return res

def sign_in():
    payload = {
        'email': 'nhatanh@gmail.com',
        'password': '123456789'
    }
    res = SDK.sign_in(**payload)
    return res

def edit_profile():
    pass