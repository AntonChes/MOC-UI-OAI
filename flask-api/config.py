import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SERVICE_NAME = 'flask-api-openai'

    LOGS_PATH = os.path.join(basedir, 'logs')
    PREHEADER_DATA_PATH = os.path.join(basedir, 'data', 'pre-headers')
    PRODUCT_JSON_DATA_PATH = os.path.join(basedir, 'data', 'products')
    THIRDBOT_JSON_DATA_FILE = os.path.join(basedir, 'data', 'third_bot.json')

    SECRET_KEY = os.environ.get("SECRET_KEY")

    REDIS_DB = os.environ.get("REDIS_DB")
    REDIS_RECORD_TTL = 600 # time to live

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False