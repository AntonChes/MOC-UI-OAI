import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

import openai


class AdvancedOpenAICompletion:
    '''
    ChatGPT is powered by gpt-3.5-turbo, OpenAI’s most advanced language model.
    Formatted with a system message first, followed by alternating user and assistant messages.
    [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        ....
    ]
    '''

    openai.api_key = os.environ.get("OPENAI_API_KEY")
    bot_name = "LogiboT+"

    def __init__(self, model="gpt-3.5-turbo") -> None:
        self.model_name = model

    def genere_text(self, 
                    messages: list, 
                    **kwargs,
                ):
        
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=messages,
            # suffix=kwargs.get('suffix', None), # suffix="only Logitech models",
            # max_tokens=kwargs.get('max_tokens', 256),
            # temperature=kwargs.get('temperature', 1.0),
            # top_p=kwargs.get('top_p', 1),
            # n=kwargs.get('n_completions', 1),
            # # stream=stream,
            # logprobs=kwargs.get('logprobs', None),
            # stop=kwargs.get('stop', None), # ["Customer", "LogiboT", "END"]
            # presence_penalty=kwargs.get('presence_penalty', 0.0),
            # frequency_penalty=kwargs.get('frequency_penalty', 0.0),
            # best_of=kwargs.get('best_of', 1),
            # logit_bias=logit_bias
        )
        
        return response.choices[0].message
    
    
def genere_messages(role: str, content: str) -> dict:
    return {"role": role, "content": content}
