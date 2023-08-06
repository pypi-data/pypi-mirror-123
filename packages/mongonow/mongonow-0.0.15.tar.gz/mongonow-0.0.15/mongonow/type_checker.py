class TypeChecker:
    @classmethod
    def _type_check(cls, v, t: tuple, name: str = None):
        if type(v) not in t:
            raise TypeError(
                '\n\t``{}``\n\tmust be of type ``{}``:\n\treceived ``{}`` instead'.format(
                    repr(v) if not name else name,
                    repr(t),
                    type(v)
                ))
