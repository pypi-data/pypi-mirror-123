import copy
from typing import Optional, Any

from mongonow.query_parser import QueryParser
from mongonow.query_tokenizer import QueryTokenizer


class FilterParser(QueryParser, QueryTokenizer):
    @classmethod
    def from_collection(cls, list_, query) -> Optional[list[tuple[int, Any]]]:
        query_ = cls._tokenize_query(query)
        return [(i, copy.deepcopy(el))
                for i, el in enumerate(list_)
                if cls._parse(el, query_)
                ] or None

