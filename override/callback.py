class Builder:

    def __new__(cls, *args, **kwargs):
        return cls._build_klass(*args, **kwargs)

    @classmethod
    def _build_klass(cls, default_builder, *args, **kwargs):
        print('hello')
        return default_builder(*args, **kwargs)
 