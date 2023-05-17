import os
import json
from collections import ChainMap
from config import Config as cfg


class BotDataReader:

    def __init__(self) -> None:
        self.json_data = self.read_json_data()

    def read_json_data(self,):
        data = list()
        file_path = os.path.join(cfg.THIRDBOT_JSON_DATA_FILE)
        with open(file_path, 'r') as filedata:
            file_json = {item['bot_name']:item for item in json.load(filedata)}
            data.append(file_json)

        return dict(ChainMap(*data))
    
    def get_data(self, name: str):
        return self.json_data[name]
    
    def get_all_thirdbot_names(self,):
        return self.json_data.keys()
    