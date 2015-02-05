from magic import Builder, wonderland


def my_callback(name, bases, attrs):
    print('from callback', name)


Builder.register_metaclass_callback(my_callback)


with wonderland(Builder):
    class Meta(type):
        def __new__(cls, name, bases, attrs):
            print('from basic!', name)
            return super().__new__(cls, name, bases, attrs)
    
    class Hueta(Meta):
        def __new__(cls, name, bases, attrs):
            print('from extended!', name)
            return super().__new__(cls, name, bases, attrs)

    
    class A(metaclass=Hueta):
        pass
    
    class B(A):
        pass

    class C(B):
        pass
