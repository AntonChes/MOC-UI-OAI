# import traceback
import time
import random
from flask import Blueprint, jsonify, request
from healthcheck import HealthCheck
from celery import chain

from .celery_worker.tasks import send_gpt_request_task
from .auth import token_required


def construct_blueprint(logger_api):
    api_bp = Blueprint("api_bp", __name__)

    # Route to expose health information
    health = HealthCheck()
    api_bp.add_url_rule('/health', 'health', view_func=lambda: health.run())

    # check celery task
    from api.celery_worker.check_task import check_tasks_bp
    api_bp.register_blueprint(check_tasks_bp)

    @api_bp.route("/chat-completion", methods=['POST'])
    @token_required
    def api_chat_completion():
        # (i.e. /chat-completion?apikey=<API_KEY>)
        # apikey = request.args.get('apikey')
        request_data = request.get_json()
        chat_id_orig = request_data.get("chat_id")
        bot_name = request_data.get("role")
        # session_id only for one request
        if bot_name == 'bloomsybox':
            chat_id = f"{bot_name}:{chat_id_orig}-{random.randint(9999,999999)}"
        else:
            chat_id = chat_id_orig
        injection = request_data.get("injection_flag")

        starttime = time.perf_counter()
        # logger_api.info(f'BEFORE API_REQUEST | {chat_id} | start time: {starttime}')

        from models import ThirdBot
        db_bot = ThirdBot.query.filter_by(bot_name=bot_name).first()
        if not db_bot:
            return jsonify({"status": "FAILED", "message": "can't find third bot name (role)"}), 400
        db_bot = {
            'bot_name': db_bot.bot_name,
            'token': db_bot.token,
            'callback_url': db_bot.callback_url
        }

        from models import PreHeader
        db_preheader = PreHeader.query.filter_by(full_name=injection).first()
        if not db_preheader:
            return jsonify({"status": "FAILED", "message": "can't find preheader"}), 400
        db_preheader = {
            'full_name': db_preheader.full_name,
            'content': db_preheader.content,
        }

        tasks = [
            send_gpt_request_task.si(chat_id_orig, chat_id, request_data, bot_name, db_bot, db_preheader, starttime),
        ]

        logger_api.info(f'API_REQUEST | request_data: {request_data}')
        ch = chain(*tasks).delay()
        return jsonify({"job_id": ch.task_id, "status": "STARTED"}), 200

    @api_bp.route("/dev/test_callback/<chat_id>", methods=['GET','POST'])
    def dev_test_train_callback(chat_id):
        request_data = request.get_json()
        job_id = request_data.get("job_id")

        logger_api.info(f'CALLBACK | /dev/test_callback/ | {request_data}')
        return jsonify(True)

    return api_bp

# @api_bp.after_request
# def after_request(response):
#     logger_api.debug('%s %s %s %s %s', request.remote_addr, request.method, request.scheme, request.full_path, response.status)
#     # app_logger.debug('Headers: %s', request.headers)
#     # app_logger.debug('Body: %s', request.get_data())
#     return response

# @api_bp.errorhandler(Exception)
# def exceptions(e):
#     tb = traceback.format_exc()
#     logger_api.debug('%s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', request.remote_addr, request.method, request.scheme, request.full_path, tb)
#     # app_logger.debug('Headers: %s', request.headers)
#     # app_logger.debug('Body: %s', request.get_data())
#     return str(e)