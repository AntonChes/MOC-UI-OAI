import os
import time
from celery import Celery, Task

# .env file
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from redis_db.model_chat_history_advanced import RedisChatHistoryADV
from open_ai.advanced_completion import AdvancedOpenAICompletion, genere_messages
from open_ai.processed.read_preheaders import read_preheader_file
from service.botdata_reader import BotDataReader
from .send_request_thirdbot import send_status

# Celery config
celery_app = Celery(__name__)
celery_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery_app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
celery_app.conf.worker_concurrency = int(os.environ.get("CELERY_CONCURRENCY", 4))
celery_app.conf.update(result_extended=True)


bot_reader = BotDataReader()

class GPTRequesTask(Task):
    name = "send_gpt_request"

    def __init__(self, chat_id_orig, chat_id, data, third_bot, db_bot=None, db_preheader=None, starttime=None) -> None:
        self.chat_id = chat_id
        self.data = data
        self.res = None
        self.chat_id_orig = chat_id_orig
        self.starttime = starttime
        self.hist = RedisChatHistoryADV(session_id=self.chat_id)
        # 
        if db_bot:
            self.third_bot_info = db_bot
        else:
            self.third_bot_info = bot_reader.get_data(third_bot)

        self.db_preheader = db_preheader['content']

    def run(self, *args, **kwargs):
        message = self.data.get("message")
        injection = self.data.get("injection_flag")
        bot_type = self.data.get("role")

        if self.hist._is_exist():
            messages = genere_messages(role="user", content=message)
            self.hist.update_messages(input_data=messages)
        else:
            if self.db_preheader:
                preheader = self.db_preheader
            else:
                preheader_file = f"{self.third_bot_info['bot_name'].lower()}/{injection}.txt"
                if self.third_bot_info['bot_name'] == 'tboty': #DEV USAGE
                    preheader_file = f"infobip/{injection}.txt"#DEV USAGE
                preheader = read_preheader_file(filename=preheader_file)
            instruction = [{"role": "system", "content": preheader}]

            self.hist.create_record(default_messages=instruction)
            messages = genere_messages(role="user", content=message)
            self.hist.update_messages(input_data=messages)

            if self.data.get("motherName") not in ["", None] and self.data.get("senderName") not in ["", None]:
                messages = genere_messages(role="user", content="for {MOTHER_NAME} and sign it '{SENDER}'".format(MOTHER_NAME=self.data.get("motherName"), SENDER=self.data.get("senderName")))
                self.hist.update_messages(input_data=messages)
            elif self.data.get("senderName") not in ["", None]:
                messages = genere_messages(role="user", content="and add the signature of the sender at the end: '{SENDER}'".format(SENDER=self.data.get("senderName")))
                self.hist.update_messages(input_data=messages)
            elif self.data.get("motherName") not in ["", None]:
                messages = genere_messages(role="user", content="for {MOTHER_NAME}, end the message with greetings and do not add to the end a signature or placeholder of the sender".format(MOTHER_NAME=self.data.get("motherName")))
                self.hist.update_messages(input_data=messages)

        messages = self.hist.get_messages()
        self.res = AdvancedOpenAICompletion().genere_text(
                messages=messages,
                temperature=0.9,
                frequency_penalty=0.5
            )

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        total_time = time.perf_counter() - self.starttime
        time_in_ms = int(total_time * 1000)
        send_status(
                    endpoint=self.third_bot_info['callback_url'],
                    job_id=task_id,
                    chat_id=self.chat_id_orig,
                    status="FAILURE",
                    time=time_in_ms
        )
        send_status(
            endpoint="http://flask:5000/api/dev/test_callback",
            job_id=task_id,
            chat_id=self.chat_id_orig,
            status="FAILURE",
            time=time_in_ms
        )
        # raise Exception(str(einfo))

    def on_success(self, retval, task_id, args, kwargs):
        total_time = time.perf_counter() - self.starttime
        time_in_ms = int(total_time * 1000)

        messages = genere_messages(role="assistant", content=self.res['content'])
        self.hist.update_messages(input_data=messages)
        send_status(
                    endpoint=self.third_bot_info['callback_url'],
                    job_id=task_id,
                    text_completion=messages['content'],
                    chat_id=self.chat_id_orig,
                    status="SUCCESS",
                    time=time_in_ms
        )
        # duble for logs
        send_status(
            endpoint="http://flask:5000/api/dev/test_callback",
            job_id=task_id,
            text_completion=messages['content'],
            chat_id=self.chat_id_orig,
            status="SUCCESS",
            time=time_in_ms
        )


@celery_app.task()
def send_gpt_request_task(chat_id_orig, chat_id, data, third_bot, db_bot, db_preheader, starttime):
    task = celery_app.register_task(GPTRequesTask(chat_id_orig, chat_id, data, third_bot, db_bot, db_preheader, starttime))
    task.apply()

    return True