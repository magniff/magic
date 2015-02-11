import sys
import imp


class _ContextInternal:

    RELOADER_SKIP = ('builtins',)

    def __init__(self, builtins_module):
        self.builtins_backup = builtins_module.__dict__.copy()
        self.builtins = builtins_module

        self.modules_preloaded = sys.modules.keys()
        self.modules_loaded = set()

    def _register_klass_builder(self, klass_builder):
        self.klass_builder = klass_builder

    def _get_new_builder(self):
        default_builder = self.builtins_backup['__build_class__']

        def new_builder(*args, **kwargs):
            return self.klass_builder(default_builder, *args, **kwargs)

        return new_builder

    def _get_new_importer(self):
        default_importer = self.builtins_backup['__import__']

        def new_importer(module_name, *args, **kwargs):
            do_reload = (
                module_name in self.modules_preloaded and
                module_name not in self.modules_loaded and
                module_name not in self.RELOADER_SKIP
            )

            self.modules_loaded.add(module_name)

            return (
                do_reload and imp.reload(sys.modules[module_name]) or
                default_importer(module_name, *args, **kwargs)
            )

        return new_importer

    def enable(self):
        self.builtins.__build_class__ = self._get_new_builder()
        self.builtins.__import__ = self._get_new_importer()

    def disable(self):
        self.builtins.__dict__.update(self.builtins_backup)


class _ContextEntry:

    import builtins
    context = _ContextInternal(builtins_module=builtins)

    def __init__(self, klass_builder):
        self.context._register_klass_builder(klass_builder)

    def __enter__(self):
        self.context.enable()

    def __exit__(self, klass, value, tb):
        self.context.disable()
