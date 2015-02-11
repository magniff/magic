from magic import Builder, wonderland


def my_callback(name, bases, attrs):
    pass


Builder.register_metaclass_callback(my_callback)


with wonderland(Builder):
    import re
