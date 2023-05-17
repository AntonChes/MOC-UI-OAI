import os
import redis
from typing import Dict

# add .env file
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def redis_connect():
    try:
        redis_client = redis.from_url(os.environ.get('REDIS_DB'))
        redis_client.ping()
    except redis.exceptions.ConnectionError as err:
        print(f"REDIS connection error {err}")
        return None

    return redis_client 

def hgetall_redis_data(redis_key_name) -> Dict:
    redis_client = redis_connect()

    result = redis_client.hgetall(redis_key_name)

    decode_b = {key.decode('utf-8'):value.decode('utf-8') for key,value in result.items()}
    if not bool(decode_b):
        # print(f"Redis: key {redis_key_name} Not found")
        return None

    return decode_b

def clean_keys_by_prefix(key_prefix):
    """
    prefix - it's part of redis key name, like chat:<sid>

    """
    redis_client = redis_connect()

    for key in redis_client.scan_iter(key_prefix):
        redis_client.delete(key)