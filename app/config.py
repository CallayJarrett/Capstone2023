import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    UPLOAD_FOLDER = './app/static/uploads'
    SECRET_KEY = 'Sup3r$3cretkey'
    #SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', './uploads')