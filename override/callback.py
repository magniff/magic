from types import FunctionType


class _CustomType(type):

    metaclass_callback = lambda *args, **kwargs: None

    @classmethod
    def _register_callback(cls, callback):
        if isinstance(callback, FunctionType):
            cls.metaclass_callback = callback

    def __new__(cls, name, bases, attrs):
        cls.metaclass_callback(name, bases, attrs)
        return super().__new__(cls, name, bases, attrs)


class Builder:

    custom_metaclass = _CustomType

    def __new__(cls, *args, **kwargs):
        return cls._build_klass(*args, **kwargs)

    @classmethod
    def register_metaclass_callback(cls, callback):
        cls.custom_metaclass._register_callback(callback)

    @classmethod
    def _build_klass(cls, default_builder, *args, **kwargs):
        _, _, *bases = args

        if not any(base.__class__ == cls.custom_metaclass for base in bases):
            if default_builder(*args, **kwargs).__class__ == type:
                kwargs['metaclass'] = cls.custom_metaclass

        return default_builder(*args, **kwargs)
