#coding: utf-8
from django.db import models
#from sqlee.utils.django.fields import (
#    CharField, BooleanField, GenericIPAddressField, FloatField,
#    DateTimeField, ForeignKey
#    )

class Models:
    def __init__(self):
        pass

    def b(self):
        print(self.__class__)
        globals()[self.__class__.__name__].a = "a"

class C(Models):
    pass

if __name__ == "__main__":
    model = C()
    model.b()
    model.__setattr__("ccc", "c")
    print(model.ccc)
