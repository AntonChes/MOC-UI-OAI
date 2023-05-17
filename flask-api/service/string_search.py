import re


def string_search(substring, fullstring):
    if re.search(substring, fullstring):
        return True
    else:
        return False
    
def search_all_intents(full_string) -> list:
    intents = re.findall(r"~(.+?)~", full_string)
    return intents

def get_message_without_intents(fullstring):
    pattern = f'(.+?)~.+?~'
    if re.search(pattern, fullstring):
        return re.search(pattern, fullstring).group(1)
    else:
        return fullstring

def get_intent_value(intents: list, fullstring) -> dict:
    new_data = dict()
    for intent in intents:
        intent_pattern = f'~{intent}~([^~]*[^~])'
        if re.search(intent_pattern, fullstring):
            new_data[intent] = re.search(intent_pattern, fullstring).group(1)
    return new_data