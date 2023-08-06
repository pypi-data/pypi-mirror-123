from typing import Union

from mongonow.database import Database
from mongonow.path import get_last_dir


class MongoNowClient(dict):
    def __init__(self, path: Union[list[str], str]):
        super().__init__()
        self.path = [path] if type(path) == str else path if type(path) == list else []
        self._load_dbs()

    def _load_dbs(self):
        for p in self.path:
            key = get_last_dir(p)
            self[key] = Database(p)
