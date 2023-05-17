import os
import json
from collections import ChainMap
from config import Config as cfg


class ProductReader:

    def __init__(self) -> None:
        self.json_data = self.read_product_json_data()

    def read_product_json_data(self,):
        data = list()
        for filename in os.listdir(cfg.PRODUCT_JSON_DATA_PATH):
            file_path = os.path.join(cfg.PRODUCT_JSON_DATA_PATH, filename)
            with open(file_path, 'r') as filedata:
                file_json = {item['title'].lower():item for item in json.load(filedata)}
                data.append(file_json)

        return dict(ChainMap(*data))
    
    def get_product(self, name: str):
        return self.json_data[name]
    
    def get_all_names(self,):
        return self.json_data.keys()
    