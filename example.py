from magic import wonderland


def callback(builder, *args, **kwargs):
    klass = builder(*args, **kwargs)
    return klass


with wonderland(callback):
    from django.db.models import *
