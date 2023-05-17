from open_ai.advanced_completion import genere_messages
from service.string_search import string_search


def do_injection(chat_history, product_reader, string):
    """
    Serching in input string name of product.
    Then concat product info to injection 
    and update history in Redis
    """
    for p_name in product_reader.get_all_names():
        if string_search(p_name, string.lower()):
            product = product_reader.get_product(p_name)
            injection = f"{product['injection']}: {product['short_description']}"
            messages = genere_messages(
                        role="user", 
                        content=injection)
            chat_history.update_messages(input_data=messages)