import os
from config.config import DUMP_DIR


def create_dump_folder():
    if not os.path.exists(DUMP_DIR):
        os.makedirs(DUMP_DIR)
