import magic


def callback(name, bases, attrs, method):
    print(name)
    return method(name, bases, attrs)


with magic.Neverland(callback):
    class Meta(type):
        pass
    
    class A(metaclass=Meta):
        pass