# encoding: utf-8
import pymongo
from datetime import datetime


class Mongo:
    def __init__(self, db):
        self.client = pymongo.MongoClient(db)
        self.db = self.client['favicon']
        self.col = self.db["favicon"]

    def insert(self, sha1, github):
        col = self.col
        data = {
            "sha1": sha1,
            "github": github, 
            "last_modified": datetime.utcnow()
        }
        inserted_id = col.insert_one(data).inserted_id
        return inserted_id

    def query(self, sha1):
        results = self.col.find({'sha1': sha1})
        return results

    def check(self, sha1, github):
        num = self.col.count_documents({'sha1': sha1, 'github': github})
        return num
