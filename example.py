from magic import wonderland


def callback(builder, *args, **kwargs):
    func, name, *bases = args
    print('Current class is', name)
    return builder(*args, **kwargs)


with wonderland(callback):
    class A: pass
