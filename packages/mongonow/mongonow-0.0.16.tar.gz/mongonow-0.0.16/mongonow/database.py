from mongonow.collection import Collection
from mongonow.path import get_json_filenames


class Database(dict):
    def __init__(self, path: str):
        super().__init__()
        self._load_collections(path)

    def _load_collections(self, path):
        for c in get_json_filenames(path):
            self[c] = Collection(name=c, path=path)

