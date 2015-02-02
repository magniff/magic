from types import FunctionType


import magic


def treat_method(attrs, method_name):
    method = attrs[method_name]

    def new_method(self, *args, **kwargs):
        print(
            'Calling method "{method_name}" of object {instance} '
            'with args={args} and {kwargs}.'.format(
                method_name=method.__name__,
                instance=self, args=args, kwargs=kwargs
            )
        )

        return method(self, *args, **kwargs)

    attrs[method_name] = new_method


def hook(name, bases, attrs, new):

    for attr_name, attr_value in attrs.items():

        if isinstance(attr_value, FunctionType):
            treat_method(attrs, attr_name)

    return new(name, bases, attrs)


with magic.Neverland(meta_hook=hook):

    class Meta(type):
        pass

    class A(metaclass=Meta):
        def some(self):
            return 10

        def bar(self, name=None):
            return name


a = A()
a.some()
a.bar(name='helloworld')

# should return
# Calling method "some" of object <__main__.A object at 0x00000000025EFE48> with args=() and {}.
# Calling method "bar" of object <__main__.A object at 0x00000000025EFE48> with args=() and {'name': 'helloworld'}.
