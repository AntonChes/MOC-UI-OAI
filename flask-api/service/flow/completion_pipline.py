from redis_db.model_chat_history import RedisChatHistory
from open_ai.completion import genere_prompt
from open_ai.processed.read_preheaders import read_preheader_file


def run_completion_pipline(session_id, preheader_name, string) -> None:
    hist = RedisChatHistory(session_id=session_id)
    if hist._is_exist():
        prompt = genere_prompt(string)
        hist.update_prompt(string=prompt)
    else:
        preheader = read_preheader_file(filename=preheader_name+".txt")
        hist.create_record(default_prompt=preheader)
        prompt = genere_prompt(string)
        hist.update_prompt(string=prompt)    