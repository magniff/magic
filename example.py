import magic


def hook(name, bases, attrs, method_new):
    return method_new(name, bases, attrs)


with magic.Neverland(meta_hook=hook):
    import numbers