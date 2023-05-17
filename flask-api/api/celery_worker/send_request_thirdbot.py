import json
import requests


def send_status(endpoint, job_id, chat_id, text_completion=None, status=None, time=None):
    headers = {
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "job_id":job_id,
        "text_completion": text_completion,
        "status": status,
        "time": time
    })
    endpoint = f"{endpoint}/{chat_id}"
    res = requests.post(endpoint, headers=headers, data=payload, timeout=5)
    print("res", res)
    return True