class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    MONGO_URI = "mongodb://localhost:27017/story"
    IMPORT_PATH = "/tmp"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
