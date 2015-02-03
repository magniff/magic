import magic


def callback(builder, *args, **kwargs):
    _, name, *_ = args
    print(name)
    return builder(*args, **kwargs)


with magic(callback):
    from django.db.models import Model
