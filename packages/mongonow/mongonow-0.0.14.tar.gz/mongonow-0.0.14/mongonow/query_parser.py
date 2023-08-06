class QueryParser:

    @classmethod
    def _parse(cls, element, tokenized_query):
        return all(eval(x.format(element)) for x in tokenized_query)
