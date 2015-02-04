class AnalisysMeta(type):
    def __new__(cls, name, bases, attrs, *args, **kwargs):
        # some code here
        klass = super().__new__(cls, name, bases, attrs)
        return klass


class Cache:

    _cache = dict()

    @classmethod
    def lookup(cls, klass_names):
        for klass_name in klass_names:
            if klass_name in cls._cache:
                return cls._cache[klass_name]

    @classmethod
    def register(cls, metaclass_name, klass_name):
        cls._cache[metaclass_name].add(klass_name)


class Builder:

    def __new__(cls, *args, **kwargs):
        return cls._build_klass(*args, **kwargs)

    @classmethod
    def _iter_bases(cls, bases):
        yield from bases

        for base in bases:
            yield from cls._iter_bases(base.__bases__)

    @classmethod
    def _build_generic_class(cls, builder, *args, **kwargs):
        _, klass_name, *bases = args

        default_metaclass = (
            kwargs.get('metaclass') or
            cls._find_metaclass(klass_name, bases)
        )

        Cache.register(default_metaclass.__name__, klass_name)

        return builder(*args, **kwargs)

    @classmethod
    def _build_metaclass(cls, builder, *args, **kwargs):
        return builder(*args, **kwargs)

    @classmethod
    def _is_metaclass(cls, bases):
        return type in tuple(cls._iter_bases(bases))

    @classmethod
    def _find_metaclass(cls, klass_name, bases):
        return Cache.lookup(cls._iter_bases(bases))

    @classmethod
    def _build_klass(cls, default_builder, *args, **kwargs):
        _, _, *bases = args
        return (
            cls._build_metaclass(default_builder, *args, **kwargs)
                if
            cls._is_metaclass(bases)
                else
            cls._build_generic_class(default_builder, *args, **kwargs)
        )
