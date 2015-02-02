import magic


def hook(name, bases, attrs, new,  *args, **kwargs):
    print(new)
    return new(name, bases, attrs)


with magic.Neverland(meta_hook=hook):
    class Meta(type):
        pass

    class A(metaclass=Meta):
        pass
