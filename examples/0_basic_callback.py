from magic import wonderland


def callback(builder, *args, **kwargs):
    _, name, *_ = args
    print('Building class %s' % name)
    return builder(*args, **kwargs)


with wonderland(callback):
    class MyClass:
        pass
