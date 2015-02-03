import functools

DEFAULT_GLOBALS = globals()
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
        original_new_method = functools.partial(metaclass.__new__, metaclass)

        def hacked_new_method(mcls, name, bases, attrs, *args, **kwargs):
            if cls.META_HOOK is None:
                return original_new_method(name, bases, attrs, *args, **kwargs)
            else:
                return cls.META_HOOK(
                    name, bases, attrs, original_new_method, *args, **kwargs
                )

        metaclass.__new__ = hacked_new_method

    @classmethod
    def _build_metaclass(cls, klass, *args, **kwargs):

        for stage in cls.PIPELINE:
            getattr(cls, '_prepare_{stage}'.format(stage=stage))(klass)

        return klass

    @classmethod
    def build_klass(cls, *args, **kwargs):
        klass = DEFAULT_BUILDER(*args, **kwargs)
        if cls._find_type_in_bases(klass):
            # i.e. this is meta class
            return cls._build_metaclass(klass, *args, **kwargs)
        else:
            return klass


class _Context:

    __fabric_klass__ = _BuilderFabric

    def __init__(self, builtins_module):
        self.builtins_backup = builtins_module.__dict__.copy()
        self.builtins = builtins_module

    def _get_new_builder(self):
        return self.__fabric_klass__.build_klass

    def _get_new_import(self, custom_builtins):

        def new_import(name, _globals=DEFAULT_GLOBALS.copy(), *args, **kwargs):
            _globals['__builtins__'] = custom_builtins

            return self.builtins_backup['__import__'](
                name, _globals, *args, **kwargs
            )

        return new_import

    def enable(self, meta_hook):
        self.__fabric_klass__.META_HOOK = meta_hook

        self.builtins.__build_class__ = self._get_new_builder()
        self.builtins.__import__ = self._get_new_import(self.builtins)

    def disable(self):
        self.builtins.__dict__.update(self.builtins_backup)


class Neverland:

    __context_handler__ = _Context

    def __init__(self, meta_hook):
        import builtins
        self.context = self.__context_handler__(builtins_module=builtins)
        self.meta_hook = meta_hook

    def __enter__(self):
        self.context.enable(meta_hook=self.meta_hook)

    def __exit__(self, klass, value, tb):
        self.context.disable()
