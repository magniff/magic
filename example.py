from override import Builder, context


def my_callback(name, bases, attrs):
    pass


Builder.register_metaclass_callback(my_callback)


with context(Builder):
    class A:
        pass

    class B(A):
        pass
