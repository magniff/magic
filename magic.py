DEFAULT_BUILDER = __build_class__


class BuilderFabric:
    
    PIPELINE = ['new',]
    
    
    @classmethod
    def _find_type_in_bases(cls, klass):
        bases = klass.__bases__

        if type in bases:
            return True
        
        for subklass in bases:
            cls._find_type_in_bases(subklass)
    
    @classmethod
    def _prepare_new(cls, klass):
        klass_new = klass.__new__

        def new_extension(cls, name, bases, attrs, *args, **kwargs):

            # ---------------
            print('This is metahack! Klass %s.' % klass.__name__)
            # ---------------

            return klass_new(klass, name, bases, attrs, *args, **kwargs)

        klass.__new__ = new_extension
    
    @classmethod
    def _prepare_metaclass(cls, klass, *args, **kwargs):

        for stage in cls.PIPELINE:
            getattr(cls, '_prepare_{stage}'.format(stage=stage))(klass)

        return klass
    
    @classmethod
    def build_klass(cls, *args, **kwargs):
        klass = DEFAULT_BUILDER(*args, **kwargs)
        print(klass.__name__)

        return (
            cls._find_type_in_bases(klass)
              and
            cls._prepare_metaclass(klass, *args, **kwargs)
              or
            klass
        )

class Builtins:

    metaclass = None

    @classmethod
    def __getitem__(cls, item_name):
        return cls._bi.get(item_name)
            
    @classmethod
    def _get_new_builder(cls):
        return BuilderFabric.build_klass

    @classmethod
    def init(cls, builtins):
        cls._bi = builtins

    @classmethod
    def enable(cls):
        cls._bi['__build_class__'] = cls._get_new_builder()
    

Builtins.init(__builtins__)


def enable():
    Builtins.enable()
