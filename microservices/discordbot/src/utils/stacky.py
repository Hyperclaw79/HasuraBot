from datetime import datetime, timedelta
from stackapi import StackAPI

class Stacky():
    def __init__(self, key, **kwargs):
        self.so = StackAPI("stackoverflow", key=key)
        for key, value in kwargs.items():
            self.so.__setattr__(key, value)

    def fetch(self, timestamp=(datetime.utcnow() - timedelta(days=1)), last_id=0):
        response = self.so.fetch("search", tagged="hasura;graphql-engine;prisma;postgraphile", fromdate=timestamp)
        questions = []
        for question in response["items"]:
            if question["question_id"] != last_id:
                data_dict = {}
                data_dict["title"] = question["title"]
                data_dict["question_id"] = question["question_id"]
                data_dict["creation_date"] = datetime.utcfromtimestamp(int(question["creation_date"]))
                data_dict["link"] = question["link"]
                data_dict["owner"] = question["owner"]["display_name"]            
                data_dict["thumbnail"] = question["owner"]["profile_image"]
                data_dict["tags"] = ', '.join(question["tags"])
                questions.append(data_dict)
        questions = sorted(questions, key= lambda x: int(x["question_id"]))
        return questions