from datetime import datetime

from .func import hgetall_redis_data, redis_connect
from config import Config as cfg

class RedisChatHistory:

    redis_client = redis_connect()

    def __init__(self, session_id):
        self.redis_key_name = f"chat:{session_id}"
        self.session_id = session_id
        # self.redis_client.expire(self.redis_key_name, cfg.REDIS_RECORD_TTL)

    def update_time(self,):
        cur_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.redis_client.hset(self.redis_key_name, 'last_update', cur_time)

    def create_record(self, default_prompt: str):
        self.redis_client.hset(self.redis_key_name, 'session_id', self.session_id)
        self.redis_client.hset(self.redis_key_name, 'prompt', default_prompt)
        self.update_time()

    def get_prompt(self,) -> str:
        return self.redis_client.hget(self.redis_key_name, 'prompt').decode("utf-8")

    def update_prompt(self, string: str):
        prompt = self.get_prompt()
        new_prompt = prompt + string
        self.redis_client.hset(self.redis_key_name, 'prompt', new_prompt)
        self.update_time()

    def _is_exist(self,):
        if hgetall_redis_data(self.redis_key_name):
            return True
        return False