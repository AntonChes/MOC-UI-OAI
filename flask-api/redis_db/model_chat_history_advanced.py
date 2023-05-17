import json
from datetime import datetime

from .func import hgetall_redis_data, redis_connect
from config import Config as cfg

class RedisChatHistoryADV:

    redis_client = redis_connect()

    def __init__(self, session_id):
        self.redis_key_name = f"adv-chat:{session_id}"
        self.session_id = session_id
        # self.redis_client.expire(self.redis_key_name, cfg.REDIS_RECORD_TTL)

    def update_time(self,):
        cur_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.redis_client.hset(self.redis_key_name, 'last_update', cur_time)

    def create_record(self, default_messages: list):
        self.redis_client.hset(self.redis_key_name, 'session_id', self.session_id)
        self.redis_client.hset(self.redis_key_name, 'messages', json.dumps(default_messages))
        self.redis_client.hset(self.redis_key_name, 'was_displayed_card', json.dumps([]))
        self.update_time()

    def get_messages(self,) -> list:
        return json.loads(self.redis_client.hget(self.redis_key_name, 'messages').decode("utf-8"))

    def update_messages(self, input_data: dict):
        messages = self.get_messages()
        messages.append(input_data)
        self.redis_client.hset(self.redis_key_name, 'messages', json.dumps(messages))
        self.update_time()

    def set_displayed_card(self, card_data):
        displayed_list = self.get_displayed_card()
        displayed_list.append(card_data)
        self.redis_client.hset(self.redis_key_name, 'was_displayed_card', json.dumps(displayed_list))
        self.update_time()
    
    def get_displayed_card(self,) -> list:
        return json.loads(self.redis_client.hget(self.redis_key_name, 'was_displayed_card').decode("utf-8"))

    def _is_exist(self,):
        if hgetall_redis_data(self.redis_key_name):
            return True
        return False
    
    def _delete(self,):
        self.redis_client.delete(self.redis_key_name)