from .func import redis_connect


class Redis3thdBotInfo:

    redis_client = redis_connect()

    def __init__(self, bot_role):
        self.redis_key_name = f"3td-bot-info:{bot_role}"
        self.bot_name = bot_role

    def get_token(self,) -> str:
        return self.redis_client.hget(self.redis_key_name, 'token').decode("utf-8")