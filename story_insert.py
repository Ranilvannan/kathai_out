import os
import json
from flask_pymongo import PyMongo

mongo = PyMongo()


class StoryInsert:

    def __init__(self, path):
        self.path = path

    def trigger_import(self):
        files = self.get_json_files()

        for file in files:
            insert_list, update_list = self.get_json_data(file)
            self.bulk_insert(insert_list)
            self.update_story(update_list)

    def bulk_insert(self, recs):
        if recs:
            mongo.db.hindi.insert_many(recs)

    def update_story(self, recs):
        for rec in recs:
            mongo.db.hindi.find_one_and_replace({"story_id": rec["story_id"]}, rec)

    def get_json_data(self, file):
        insert_list = []
        update_list = []

        with open(file) as json_file:
            recs = json.load(json_file)
            if isinstance(recs, list):
                for rec in recs:
                    res = mongo.db.hindi.find({"story_id": rec["story_id"]}).count()
                    if res:
                        update_list.append(rec)
                    else:
                        insert_list.append(rec)

        return insert_list, update_list

    def get_json_files(self):
        list_files = os.listdir(self.path)
        xml_list = []

        for item in list_files:
            if item.endswith(".json"):
                file_path = os.path.join(self.path, item)
                xml_list.append(file_path)

        return xml_list
