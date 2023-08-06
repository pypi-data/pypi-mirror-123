from mongonow.filter_parser import FilterParser
from mongonow.json_manager import JsonManager

class Collection(list):
    def __init__(self, name, path):
        super().__init__()
        self.extend(JsonManager.load_collection(path, name))

    def find_one(self, query: dict):
        res = FilterParser.from_collection(self, query)
        return res[0][1] if res else None

    def insert_one(self, document):
        self._check_id_and_insert(document)
        return self[len(self) - 1]

    def update_one(self, query: dict, document: dict):
        i, d = FilterParser.from_collection(self, query)[0]
        [d.__setitem__(k, v) for k, v in document.items()]
        self[i] = d
        return self[i]

    def delete_one(self, query):
        i, _ = FilterParser.from_collection(self, query)[0]
        return self.pop(i)

    def find(self, query):
        res = FilterParser.from_collection(self, query)
        return [x[1] for x in res] if res else None

    def insert_many(self, documents):
        i = len(self)
        [self._check_id_and_insert(d) for d in documents]
        return self[i:]

    def update_many(self, query, document):
        idx = []
        for i, d in FilterParser.from_collection(self, query):
            [d.__setitem__(k, v) for k, v in document.items()]
            self[i] = d
            idx.append(i)
        return [self[i] for i in idx]

    def delete_many(self, query):
        return [self.pop(i) for i, _ in FilterParser.from_collection(self, query)]

    def _check_id_and_insert(self, doc):
        if not doc.get('_id'):
            doc['_id'] = self._get_new_id()
        self.append(doc)

    def _get_new_id(self):
        return len(self)

