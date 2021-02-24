from odoo import models, fields
from odoo.tools import config
import xml.etree.ElementTree as et
import os
import pymongo

PATH = config["kathai_out_import_path"]
MONGO_URI = config["kathai_out_mongo_uri"]


class KathaiOuImport(models.TransientModel):
    _name = "kathai.out.import"
    _description = "Story Import"

    name = fields.Char(string="Name")

    def trigger_import(self):
        file_list = self.get_xml_files(PATH)

        for files in file_list:
            stories = self.get_story_content(files)
            story_obj = self.env["kathai.out.story"].create(stories)
            self.update_mongodb(story_obj)

    def update_mongodb(self, recs):
        cli = pymongo.MongoClient(MONGO_URI)
        db = cli["kathai_client"]
        col = db["story"]

        for rec in recs:
            col.delete_many({"title": rec.title})

        story_list = [{"title": rec.title, "record_id": rec.id} for rec in recs]

        if story_list:
            col.insert_many(story_list)

    def check_and_remove_story(self, seq):
        recs = self.env["kathai.out.story"].search([("sequence", "=", seq)])
        if recs:
            recs.unlink()

        return True

    def get_xml_files(self, path):
        list_files = os.listdir(path)
        xml_list = []

        for item in list_files:
            if item.endswith(".xml"):
                file_path = os.path.join(path, item)
                xml_list.append(file_path)

        return xml_list

    def get_story_content(self, file_name):
        tree = et.parse(file_name)
        page = tree.getroot()

        story_list = []
        stories = page.findall("story")

        for story in stories:
            title = story.find("title").text
            preview = story.find("preview").text
            sequence = story.find("sequence").text
            paragraphs = story.findall("content")

            content = [(0, 0, {"order_seq": int(rec.attrib.get("order_seq", 0)),
                        "paragraph": rec.text}) for rec in paragraphs]

            self.check_and_remove_story(sequence)

            story_list.append({"sequence": sequence,
                               "title": title,
                               "preview": preview,
                               "content_ids": content})
        return story_list




