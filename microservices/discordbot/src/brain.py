import requests
import json

class HyperAI:
    def __init__(self, user, key, nick=None):
        self.user = user
        self.key = key
        self.nick = nick
        self.sess = requests.Session()
        body = {
            'user': user,
            'key': key,
            'nick': nick
        }
        self.sess.post('https://cleverbot.io/1.0/create', json=body)


    def query(self, text):
        body = {
            'user': self.user,
            'key': self.key,
            'nick': self.nick,
            'text': text
        }

        r = self.sess.post('https://cleverbot.io/1.0/ask', json=body)
        r = json.loads(r.text)

        if r['status'] == 'success':
            return r['response']
        else:
            return False
