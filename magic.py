class _Context:

    def __init__(self, builtins_module):
        self.builtins_backup = builtins_module.__dict__.copy()
        self.builtins = builtins_module

    def _register_klass_builder(self, klass_builder):
        self.klass_builder = klass_builder

    def _get_new_builder(self):
        default_builder = self.builtins_backup['__build_class__']

        def new_builder(*args, **kwargs):
            return self.klass_builder(default_builder, *args, **kwargs)

        return new_builder

    def enable(self):
        self.builtins.__build_class__ = self._get_new_builder()

    def disable(self):
        self.builtins.__dict__.update(self.builtins_backup)


class Neverland:

    import builtins
    context = _Context(builtins_module=builtins)

    def __init__(self, klass_builder):
        self.context._register_klass_builder(klass_builder)

    def __enter__(self):
        self.context.enable()

    def __exit__(self, klass, value, tb):
        self.context.disable()
