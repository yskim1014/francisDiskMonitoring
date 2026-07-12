# Call by import
import requests as req
from datetime import datetime
from datetime import timedelta
import jwt
import json

# Bot handling
class Bot:
    def __init__(self):
        self.__client_id = ''
        self.__client_secret = ''
        self.__service_account = ''
        self.__bot_id = ''
        self.__headers = {'Content-Type': 'application/json'}
        self.__baseurl = ''
        with open('-pk.key', 'rb') as f:
            self.__private_key = f.read()

    @property
    def client_id(self):
        return self.__client_id
    @client_id.setter
    def client_id(self, client_id):
        self.__client_id = client_id
    @property
    def client_secret(self):
        return 'client_secret은 조회할 수 없습니다.'
    @client_secret.setter
    def client_secret(self, client_secret):
        self.__client_secret = client_secret
    @property
    def service_account(self):
        return self.__service_account
    @service_account.setter
    def service_account(self, service_account):
        self.__service_account = service_account
    @property
    def bot_id(self):
        return self.__bot_id
    @bot_id.setter
    def bot_id(self, bot_id):
        self.__bot_id = bot_id
    @property
    def headers(self):
        return 'headers는 조회할 수 없습니다.'

    def assertion(self):
        payload = {
          "iss":self.__client_id,
          "sub":self.__service_account,
          "iat":int(datetime.timestamp(datetime.now())),
          "exp":int(datetime.timestamp(datetime.now() + timedelta(hours=1)))
        }
        assertion_data = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'client_id': self.__client_id,
            'client_secret': self.__client_secret,
            'assertion': jwt.encode(payload = payload, key = self.__private_key, algorithm = 'RS256'),
            'scope': 'bot user.read',
        }
        res = req.post('https://auth.worksmobile.com/oauth2/v2.0/token', data=assertion_data).json()
        self.__headers['Authorization'] = 'Bearer ' + res['access_token']

    def get_user_id(self, *user_email:tuple[str]):
        res = req.get(url = self.__baseurl + 'users', headers = self.__headers)
        users = {user['email'].split('@')[0]: user['userId'] for user in res.json()['users']}
        return tuple(users.get(user, '-') for user in user_email)

    def send_message(self, text:str, users:tuple, i18ntexts:list[dict[str, str]]='') -> list[req.Response]:
        contents = {"content": {"type": "text", "text": text}}
        if i18ntexts:
            contents['i18nTexts'] = i18ntexts # "i18nTexts": [{"language": "ja_JP","text": "こんにちは"},{"language": "ko_KR", "text": "안녕하세요"}]
        messages_urls = (f'bots/{self.__bot_id}/users/{user}/messages' for user in users)
        return [req.post(url = self.__baseurl + messages_url, headers = self.__headers, data=json.dumps(contents)) for messages_url in messages_urls]
