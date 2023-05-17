from flask_socketio import emit
from service.string_search import string_search


def product_img_to_chat(product_reader, string):
    for p_name in product_reader.get_all_names():
        if string_search(p_name, string.lower()):
            emit('image found', product_reader.get_product(p_name)['imgUrl'])

def product_card_to_chat(product_reader, string):
    for p_name in product_reader.get_all_names():
        if string_search(p_name, string.lower()):
            emit('product card', product_reader.get_product(p_name))

def shoppingcart_card_to_chat():
    emit('shopping-cart card')
