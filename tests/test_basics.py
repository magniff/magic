from magic import wonderland


# add some attrs
def test_basic():

    def builder(default_builder, *args, **kwargs):
        klass = default_builder(*args, **kwargs)
        klass.foo = 'helloworld'
        return klass

    with wonderland(builder):
        class A:
            pass

    class B:
        pass

    assert A.foo == 'helloworld'
    assert not hasattr(B, 'foo')


# pass custom meta class
def test_with_meta():

    class MyMeta(type):
        def __new__(cls, name, bases, attrs):
            klass = super().__new__(cls, name, bases, attrs)
            klass.bar = 'meta'
            return klass

    def builder(default_builder, *args, **kwargs):
        kwargs['metaclass'] = MyMeta
        klass = default_builder(*args, **kwargs)
        return klass

    with wonderland(builder):
        class A:
            pass

    class B:
        pass

    assert A.bar == 'meta'
    assert not hasattr(B, 'bar')
