from main import db
from sqlalchemy.sql import func
import json

class ThirdBot(db.Model):
    __tablename__ = 'third_bot'

    id = db.Column(db.Integer, primary_key=True)
    bot_name = db.Column(db.String(100), nullable=False)
    callback_url = db.Column(db.String(256), nullable=False)
    token = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __init__(self, name, token, callback_url):
        self.bot_name = name
        self.token = token
        self.callback_url

    def __repr__(self):
        return f'<ThirdBot {self.bot_name}>'


class PreHeader(db.Model):
    __tablename__ = 'pre_header'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __init__(self, name, content):
        self.full_name = name
        self.content = content

    @staticmethod
    def delete_rec(data_rec):
        db.session.delete(data_rec)#.delete
        db.session.commit()

    def __repr__(self):
        return f'<PreHeader content: {self.content}>'