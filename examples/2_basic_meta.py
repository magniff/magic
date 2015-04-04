from magic import wonderland


class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        print('hello from metaclass %s' % cls.__name__)
        return super().__new__(cls, name, bases, attrs)


def callback(builder, *args, **kwargs):
    kwargs['metaclass'] = MyMeta
    return builder(*args, **kwargs)


with wonderland(callback):
    class MyClass:
        pass
