import os


class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    MONGO_URI = os.environ.get("MONGO_URI")
    IMPORT_PATH = os.environ.get("IMPORT_PATH")


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
