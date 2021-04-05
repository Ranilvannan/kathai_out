import os
import json
from flask_pymongo import PyMongo

mongo = PyMongo()


class DataInsert:

    def __init__(self, path, param_key, filename):
        self.path = path
        self.param_key = param_key
        self.filename = filename

    def trigger_import(self):
        files = self.get_json_files()

        for file in files:
            insert_list, update_list = self.get_json_data(file)
            self.bulk_insert(insert_list)
            self.update_data(update_list)

            if os.path.exists(file):
                os.remove(file)

    def bulk_insert(self, recs):
        if recs:
            mongo.db.english_story.insert_many(recs)

    def update_data(self, recs):
        for rec in recs:
            params = {self.param_key: rec[self.param_key]}
            mongo.db.english_story.find_one_and_replace(params, rec)

    def get_json_data(self, file):
        insert_list = []
        update_list = []

        with open(file) as json_file:
            recs = json.load(json_file)
            if isinstance(recs, list):
                for rec in recs:
                    params = {self.param_key: rec[self.param_key]}
                    res = mongo.db.english_story.find(params).count()
                    if res:
                        update_list.append(rec)
                    else:
                        insert_list.append(rec)

        return insert_list, update_list

    def get_json_files(self):
        list_files = os.listdir(self.path)
        xml_list = []

        for item in list_files:
            filename = self.filename
            if item.endswith(filename):
                file_path = os.path.join(self.path, item)
                xml_list.append(file_path)

        return xml_list
