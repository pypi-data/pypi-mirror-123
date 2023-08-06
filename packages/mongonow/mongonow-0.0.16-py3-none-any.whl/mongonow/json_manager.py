import json


class JsonManager:
    _path_pattern = '{}/{}.json'

    @classmethod
    def load_collection(cls, path, name):
        with open(cls._path_pattern.format(path, name)) as f:
            data = json.load(f)
        return data[name]

    @classmethod
    def dump_collection(cls, obj, file_path):
        json.dump(obj, file_path)
