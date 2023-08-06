from typing import Any

from mongonow.type_checker import TypeChecker


class QueryTokenizer(TypeChecker):
    comparison_query_selector_set = {'$eq', '$gt', '$gte', '$in', '$lt', '$lte', '$ne', '$nin'}
    logical_query_selector_set = {'$and', '$not', '$nor', '$or'}
    comparison_query_selector_lexicon = {
        '$eq': '==',
        '$gt': '>',
        '$gte': '>=',
        '$in': 'in',
        '$lt': '<',
        '$lte': '<=',
        '$ne': '!=',
        '$nin': 'not in'
    }

    @classmethod
    def _tokenize_query(cls, query: dict[str, Any]):
        tokenized_expr = []
        cls._type_check(query, (dict,))
        for k, v in query.items():
            if k.startswith('$'):
                tokenized_expr.append(cls._tokenize_query_selector(k, v))
            else:
                tokenized_expr.append(cls._tokenize_fields(k, v))
        return tokenized_expr

    @classmethod
    def _tokenize_list(cls, _list: list):
        """ returns a list of expressions """
        tokenized_expr = []
        for x in _list:
            cls._type_check(x, (dict,))
            for k, v in x.items():
                if k.startswith('$'):
                    tokenized_expr.append(cls._tokenize_query_selector(k, v))
                tokenized_expr.append(cls._tokenize_fields(k, v))
        return tokenized_expr

    @classmethod
    def _tokenize_fields(cls, k, v):
        """
        key.split('.')
        put every split subfields b/w brackets
        field = {}[subfield_0][subfield_1][...]

        if type(v) is int/str/float => It's an implicit equality comparison
        if type(v) is dict => We get the comparison expr & value of the nested k_ & v_
        :return str
        """
        subfields = k.split('.')
        brackets = ('["{}"]' * subfields.__len__()).format(*subfields)
        field = '{0}' + brackets
        if type(v) in {str, int, float}:
            return " ".join([field, "==", str(v)])
        if type(v) == dict:
            k_, v_ = list(v.items())[0]
            if k_ in cls.comparison_query_selector_set:
                return " ".join([field, cls._tokenize_comparison_query_selector(k_, v_)])

    @classmethod
    def _tokenize_query_selector(cls, k, v):
        if k in cls.comparison_query_selector_set:
            return cls._tokenize_comparison_query_selector(k, v)
        if k in cls.logical_query_selector_set:
            return cls._tokenize_logical_query_selector(k, v)
        raise ValueError("Query selector ``{}`` not supported.".format(k))

    @classmethod
    def _tokenize_comparison_query_selector(cls, k, v):
        cls._type_check(v=v, t=(str, int, float))
        return " ".join([cls.comparison_query_selector_lexicon[k], str(v)])

    @classmethod
    def _tokenize_logical_query_selector(cls, k, v):
        if k == '$and':
            return cls._tokenize_and(v)
        if k == '$or':
            return cls._tokenize_or(v)
        if k == '$nor':
            return cls._tokenize_nor(v)
        if k == '$not':
            return cls._tokenize_not(v)
        raise ValueError("Query selector ``{}`` not supported.".format(k))

    @classmethod
    def _tokenize_and(cls, v):
        """ ' and '.join([]) """
        cls._type_check(v=v, t=(list,),)
        return " and ".join(cls._tokenize_list(v))

    @classmethod
    def _tokenize_or(cls, v):
        """ ' or '.join([]) """
        cls._type_check(v=v, t=(list,), )
        return " or ".join(cls._tokenize_list(v))

    @classmethod
    def _tokenize_nor(cls, v):
        """ 'not ' + cls.tokenize_or(k,v) """
        cls._type_check(v=v, t=(list,))
        return "not " + cls._tokenize_or(v)

    @classmethod
    def _tokenize_not(cls, v):
        """ "not" + tokenize(v) """
        cls._type_check(v=v, t=(dict,))
        return 'not ' + cls._tokenize_query(v)[0]
