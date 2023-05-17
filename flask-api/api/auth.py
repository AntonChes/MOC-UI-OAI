from flask import request, jsonify
from functools import wraps

from redis_db.model_bot_info import Redis3thdBotInfo


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        
        request_data = request.get_json()
        bot_name = request_data.get("role")
        bot_info = Redis3thdBotInfo(bot_name)
        from models import ThirdBot
        bot_info = ThirdBot.query.filter_by(bot_name=bot_name).first()

        try:
            current_bot_token = bot_info.token
            if current_bot_token != token:
                raise Exception('token is invalid')
        except:
            return jsonify({'message': 'token is invalid'})

        return f(*args, **kwargs)
    return decorator