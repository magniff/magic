from functools import partial
DEFAULT_BUILDER = __build_class__


class _BuilderFabric:

    PIPELINE = ('new',)
    META_HOOK = None

    @classmethod
    def _find_type_in_bases(cls, klass):
        bases = klass.__bases__
        return type in bases or any(map(cls._find_type_in_bases, bases))

    @classmethod
    def _prepare_new(cls, metaclass):
        original_new_method = partial(metaclass.__new__, metaclass)

        def hacked_new_method(mcls, name, bases, attrs, *args, **kwargs):
            return cls.META_HOOK(
                name, bases, attrs, original_new_method, *args, **kwargs
            )

        metaclass.__new__ = hacked_new_method

    @classmethod
    def _prepare_metaclass(cls, klass, *args, **kwargs):

        for stage in cls.PIPELINE:
            getattr(cls, '_prepare_{stage}'.format(stage=stage))(klass)

        return klass

    @classmethod
    def build_klass(cls, *args, **kwargs):
        klass = DEFAULT_BUILDER(*args, **kwargs)

        return (
            cls._find_type_in_bases(klass)
              and
            cls._prepare_metaclass(klass, *args, **kwargs)
              or
            klass
        )


class _Builtins:

    __bi_copy__ = None
    __fabric__ = _BuilderFabric

    @classmethod
    def __getitem__(cls, item_name):
        return cls._bi.get(item_name)

    @classmethod
    def _get_new_builder(cls):
        return cls.__fabric__.build_klass

    @classmethod
    def init(cls, builtins):
        cls.__bi_copy__ = builtins.copy()
        cls._bi = builtins

    @classmethod
    def enable(cls, meta_hook):
        cls._bi['__build_class__'] = cls._get_new_builder()
        cls.__fabric__.META_HOOK = meta_hook

    @classmethod
    def disable(cls):
        cls._bi.update(cls.__bi_copy__)


class Neverland:
    def __init__(self, meta_hook):
        self.meta_hook = meta_hook

    def __enter__(self):
        _Builtins.init(__builtins__)
        _Builtins.enable(meta_hook=self.meta_hook)

    def __exit__(self, klass, value, tb):
        _Builtins.disable()
