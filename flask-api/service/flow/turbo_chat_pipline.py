from service.string_search import string_search
from redis_db.model_chat_history_advanced import RedisChatHistoryADV
from open_ai.advanced_completion import genere_messages
from open_ai.processed.injection import do_injection


def run_turbo_pipline(product_reader, session_id, bot_instruction, string) -> None:
    hist = RedisChatHistoryADV(session_id=session_id)
    if hist._is_exist():
        messages = genere_messages(role="user", content=string)
        hist.update_messages(input_data=messages)

        # injection
        if string_search('additional info about', string.lower()) or \
            string_search('additional information about', string.lower()) or \
            string_search('additional info', string.lower()):
            do_injection(chat_history=hist, product_reader=product_reader, string=string)
                    
    else:
        instruction = [{"role": "system", "content": bot_instruction}]
        hist.create_record(default_messages=instruction)
        messages = genere_messages(role="user", content=string)
        hist.update_messages(input_data=messages)
