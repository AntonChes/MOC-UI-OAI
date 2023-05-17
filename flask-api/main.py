import numpy as np
from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_session import Session
from flask_uuid import FlaskUUID
from flask_sqlalchemy import SQLAlchemy

import logging
from loger import setup_logger

from redis_db.model_chat_history import RedisChatHistory
from redis_db.model_chat_history_advanced import RedisChatHistoryADV

from open_ai.completion import OpenAICompletion
from open_ai.advanced_completion import AdvancedOpenAICompletion
from service.string_search import string_search, search_all_intents, get_intent_value, get_message_without_intents
from service.product_reader import ProductReader
from service.structured_content import product_img_to_chat, product_card_to_chat, shoppingcart_card_to_chat

from service.flow.turbo_chat_pipline import run_turbo_pipline
from service.flow.completion_pipline import run_completion_pipline


app = Flask(__name__)
app.config.from_object("config.Config")

Session(app)
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

FlaskUUID(app)

# preheaders db
db = SQLAlchemy(app)

# read products info
try:
    products_data = ProductReader()
except Exception as err:
    print(err, "Cant read products")

# ===== Logs =====
logger_chat = setup_logger('logger_chat', f'{app.config["LOGS_PATH"]}/chat.log', level=logging.DEBUG)
logging.basicConfig(filename=f'{app.config["LOGS_PATH"]}/flask.log',level=logging.DEBUG)
logger_api = setup_logger('logger_api', f'{app.config["LOGS_PATH"]}/api.log', level=logging.DEBUG)

# ===== Register Routes =====
from routes.chat import chat_page
from routes.chat_advanced import chat_advanced_page

from routes import preheader_page
from routes import thirdbot_page

from api import api_routes as api_bp

from routes.errors import err_page
app.register_blueprint(err_page)

app.register_blueprint(chat_page)
app.register_blueprint(chat_advanced_page)
app.register_blueprint(api_bp.construct_blueprint(logger_api), url_prefix='/api')

# from models import PreHeader
# app.register_blueprint(preheader_page.construct_blueprint(db, PreHeader), url_prefix='/preheaders')
app.register_blueprint(preheader_page.construct_blueprint(db,), url_prefix='/preheaders')

# from models import ThirdBot
# app.register_blueprint(thirdbot_page.construct_blueprint(db, ThirdBot), url_prefix='/bots')
app.register_blueprint(thirdbot_page.construct_blueprint(), url_prefix='/bots')


# ===== SocketIO =====
@socketio.on('user input', namespace='/user-input')
def receive_user_input(json):
    json['session_id'] = request.sid
    user_input = json['message']

    # tmp | parse image name from user input 
    # and add to chat
    if string_search('show', user_input.lower()): #HARDCODE
        product_img_to_chat(product_reader=products_data, string=user_input)

    else:
        run_completion_pipline(
                session_id=json['session_id'], 
                preheader_name=json['preheader_name'], 
                string=user_input
            )
    
    logger_chat.info(json)
    emit('after user input', json)

@socketio.on('request to bot')
def send_openai_req(json):
    hist = RedisChatHistory(session_id=json['session_id'])

    stop_tokens_list = json['stop'].split(", ")
    suffix = None if json['suffix'] == '' else json['suffix']

    prompt = hist.get_prompt()
    res = OpenAICompletion(model=json['model_name']).genere_text(
        prompt=prompt,
        suffix=suffix,
        max_tokens=json['max_tokens'],
        temperature=json['temperature'],
        top_p=json['top_p'],
        n_completions=json['n_completions'],
        stream=json['stream'],
        logprobs=json['logprobs'],
        stop=stop_tokens_list,
        presence_penalty=json['presence_penalty'],
        frequency_penalty=json['frequency_penalty'],
        best_of=json['best_of'],
    )
        
    json['sender_name'], json['message'] = res['sender_name'], res['message']
    hist.update_prompt(string=json['message'])

    logger_chat.info(json)
    emit('bot input', json)


# TURBO

@socketio.on('user input (turbo)', namespace='/advanced/user-input')
def receive_user_input_adv(json):
    json['session_id'] = request.sid
    bot_instruction = json['instruction']
    user_input = json['message']

    # tmp | parse image name from user input 
    # and add to chat
    # if string_search('show', user_input.lower()):
    #     product_img_to_chat(product_reader=products_data, string=user_input)

    # if string_search('product card', user_input.lower()):
    #     product_card_to_chat(product_reader=products_data, string=user_input)

    # else:
    run_turbo_pipline(
            product_reader=products_data,
            session_id=json['session_id'],
            bot_instruction=bot_instruction, 
            string=user_input
        )
    logger_chat.info(json)
    emit('after user input (turbo)', json)

@socketio.on('request to bot (turbo)', namespace='/advanced')
def send_openai_req_adv(json):
    hist = RedisChatHistoryADV(session_id=json['session_id'])

    messages = hist.get_messages()
    res = AdvancedOpenAICompletion(model=json['model_name']).genere_text(
            messages=messages,
        )

    res_intents = search_all_intents(res['content'])
    intents_value = get_intent_value(res_intents, res['content'])

    json['sender_name'], json['message'] = res['role'], get_message_without_intents(res['content'])
    json['intents'] = intents_value
    json['full_message'] = res['content']
    hist.update_messages(input_data=res)

    logger_chat.info(json)
    emit('bot input (turbo)', json)


@socketio.on('check intent', namespace='/advanced/user-input')
def send_openai_req_adv(json):
    hist = RedisChatHistoryADV(session_id=json['session_id'])
    displayed_before = hist.get_displayed_card()

    # ~DETAILS~
    if json['intents'].get('DETAILS'):
        all_entity = json['intents']['DETAILS'].strip().strip('.').split(';')
        all_entity = np.array(all_entity)
        for product in np.unique(all_entity):
            if product not in displayed_before:
                product_card_to_chat(product_reader=products_data, string=f'card for {product}')
                hist.set_displayed_card(product)
    # ~CART~
    if json['intents'].get('CART'):
        if 'shopping-cart' not in displayed_before:
            shoppingcart_card_to_chat()
            hist.set_displayed_card('shopping-cart')


@socketio.on('cleaning chat history', namespace='/advanced/user-input')
def clean_history_in_redis():
    hist = RedisChatHistoryADV(session_id=request.sid)
    hist._delete()
    logger_chat.info(f"Chat cleaning (id {request.sid})")


if __name__ == '__main__':
    db.create_all()
    socketio.run(app, host="0.0.0.0", debug=True)