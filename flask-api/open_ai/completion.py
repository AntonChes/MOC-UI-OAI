import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

import openai


class OpenAICompletion:

    openai.api_key = os.environ.get("OPENAI_API_KEY")
    bot_name = "LogiboT"

    def __init__(self, model="text-davinci-003") -> None:
        self.model_name = model

    def genere_text(self, 
                    prompt: str,
                    **kwargs,
                ):
        
        response = openai.Completion.create(
            model=self.model_name,
            prompt=prompt,
            suffix=kwargs.get('suffix', None), # suffix="only Logitech models",
            max_tokens=kwargs.get('max_tokens', 256),
            temperature=kwargs.get('temperature', 1.0),
            top_p=kwargs.get('top_p', 1),
            n=kwargs.get('n_completions', 1),
            # stream=stream,
            logprobs=kwargs.get('logprobs', None),
            stop=kwargs.get('stop', None), # ["Customer", "LogiboT", "END"]
            presence_penalty=kwargs.get('presence_penalty', 0.0),
            frequency_penalty=kwargs.get('frequency_penalty', 0.0),
            best_of=kwargs.get('best_of', 1),
            # logit_bias=logit_bias
        )            

        return {
            "sender_name": self.bot_name,
            "message": response.choices[0].text,
        }
    
    
def genere_prompt(user_input: str) -> str:
    '''
    Create prompt string where at start_sequence and restart_sequence in the string
    the API will stop generating further tokens. 
    The returned text will not contain the stop sequence.
    '''
    start_sequence = "\nLogiboT"
    restart_sequence = "\nCustomer"

    res = '{}: {}\n{}:'.format(restart_sequence, user_input, start_sequence)
    return res
