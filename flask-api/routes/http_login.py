import os
# add .env file
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


auth = HTTPBasicAuth()

users = {
    os.environ.get('ADMNAME'): generate_password_hash(os.environ.get('ADMPASS')),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username