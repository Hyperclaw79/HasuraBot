import requests

class Urban:
    def __init__(self):
        self.sess = requests.Session()
        self.url = "http://api.urbandictionary.com/v0/"

    def fetch(self, word=None):
        if word:
            url = "{}define?term={}".format(self.url, word) 
        else:    
            url = self.url+"random"
        res = self.sess.get(url).json()
        meanings = sorted(
            res['list'],
            key = lambda k:k['thumbs_up'],
            reverse=True
        )
        sortme = [
            {
                "meaning":meaning["definition"],
                "example":meaning["example"],
                "word":meaning["word"]
            } for meaning in meanings
        ]
        if not word:
            solutions = [sortme[0]]
            print(solutions)
        else:
            i = 5
            while True:
                if i <= len(sortme):
                    spliced = sortme[0:i]
                    break
                else:
                    i -= 1    
            solutions = sorted(spliced, key = lambda k:len(k["meaning"]))
        return solutions
