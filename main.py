import magic


magic.enable()

 
class A(type):
    def __new__(cls, name, bases, attrs, *args, **kwargs):
        return super().__new__(cls, name, bases, attrs, *args, **kwargs)
  
  
class SomeMeta(A):
    def __new__(cls, name, bases, attrs):
        klass = super().__new__(cls, name, bases, attrs)
        klass.some = 'foo'
        return klass



class Some(metaclass=SomeMeta):
    pass


print(Some.some)