from types import FunctionType


class _MetaMeta(type):

    metaclass_callback = lambda *args, **kwargs: None

    @classmethod
    def _register_callback(cls, callback):
        if isinstance(callback, FunctionType):
            cls.metaclass_callback = callback

    def __new__(cls, *args, **kwargs):

        metaclass = super().__new__(cls, *args, **kwargs)
        original_new = metaclass.__new__

        def hacked_new(mcls, name, bases, attrs):
            cls.metaclass_callback(name, bases, attrs)
            return original_new(mcls, name, bases, attrs)

        metaclass.__new__ = hacked_new

        return metaclass


class Builder:

    meta_meta = _MetaMeta

    def __new__(cls, *args, **kwargs):
        return cls._build_klass(*args, **kwargs)

    @classmethod
    def register_metaclass_callback(cls, callback):
        cls.meta_meta._register_callback(callback)

    @classmethod
    def _build_klass(cls, default_builder, *args, **kwargs):
        _, _, *bases = args
        if any(base.__class__ == type for base in bases):
            if 'metaclass' not in kwargs:
                kwargs['metaclass'] = cls.meta_meta

        return default_builder(*args, **kwargs)
