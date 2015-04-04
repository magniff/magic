from magic import wonderland


def callback(builder, *args, **kwargs):
    func, *_ = args
    print(func.__code__.co_consts)
    return builder(*args, **kwargs)


with wonderland(callback):
    class MyClass:
        def __init__(self):
            pass
