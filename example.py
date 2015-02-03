import magic

"CFunctionType"

from ctypes import *


def callback(builder, *args, **kwargs):
    if type in args:
        print(args[1])
    return builder(*args, **kwargs)


with magic.Neverland(callback):
    from django.db.models import Model