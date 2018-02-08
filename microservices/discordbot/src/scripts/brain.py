import json
import requests
import aiohttp

class HyperAI:
    def __init__(self, user, key, nick=None):
        self.user = user
        self.key = key
        self.nick = nick
        self.sess = aiohttp.ClientSession()
        body = {
            'user': user,
            'key': key,
            'nick': nick
        }
        requests.post('https://cleverbot.io/1.0/create', json=body)


    async def query(self, text):
        body = {
            'user': self.user,
            'key': self.key,
            'nick': self.nick,
            'text': text
        }

        async with self.sess.post('https://cleverbot.io/1.0/ask', json=body) as resp:
            r = await resp.json()

        if r['status'] == 'success':
            return r['response']
        else:
            return False
