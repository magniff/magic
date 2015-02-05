from override import Builder, context


def my_callback(name, bases, attrs):

    def __new__(cls, *args, **kwargs):
        _, parent, *_ = cls.__mro__

        if cls.instance is None:
            cls.instance = parent.__new__(parent, *args, **kwargs)

        return cls.instance

    attrs['instance'] = None
    attrs['__new__'] = __new__


Builder.register_metaclass_callback(my_callback)


with context(Builder):
    class A:
        pass

    class B(A):
        pass

    class C(B, A):
        pass


assert C() is A()
assert A() is A()
assert A() is B()
