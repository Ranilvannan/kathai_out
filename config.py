import os


class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    MONGO_URI = "mongodb://localhost:27017/story"
    IMPORT_PATH = "/var/story_reader/English"
    DATABASE = "story"
    STORY = "english_story"
    CATEGORY = "english_category"
    LANGUAGE = "English"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
