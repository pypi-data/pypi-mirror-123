import os


def get_json_filenames(path):
    return [x.split('.')[0] for x in os.listdir(path) if x.endswith('.json')]


def get_last_dir(path):
    pattern = ['/', '\\']
    return [path.split(x)[-1] for x in pattern if x in path][0]
