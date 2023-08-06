import os

BASE_DIR = os.path.split(__file__)[0]


def get_path(rel_path):
    return f'{BASE_DIR}/{rel_path}'
