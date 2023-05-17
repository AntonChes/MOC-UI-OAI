import os
from config import Config as cfg


def read_preheader_file(filename="L1.txt") -> str:
    file_path = os.path.join(cfg.PREHEADER_DATA_PATH, filename)
    with open(file_path, 'r') as file:
        data = file.read().replace('\n', '')
    
    return data