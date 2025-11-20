#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Field:
    def __set_name__(self, owner, name):
        self.name = f"_{owner.__name__}_{name}"

    def __init__(self, name=None):
        pass

    def __get__(self, instance, owner=None):
        if not instance:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)


class MetaField(type):
    def __new__(mcls, clsname, bases, clsdict):
        fields = clsdict["_fields"]
        for field in fields:
            clsdict[field] = Field()

        def __init__(self, *args, **kwargs):
            for name, val in zip(fields, args):
                self.__dict__[name] = val

        clsdict["__init__"] = __init__

        def __repr__(self):
            key_val_pairs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
            return f"{self.__class__.__name__}({key_val_pairs})"

        clsdict["__repr__"] = __repr__

        return super().__new__(mcls, clsname, bases, clsdict)


class Person(metaclass=MetaField):
    _fields = ["name", "age", "salary"]


if __name__ == "__main__":
    lara = Person("Elara Vance", 34, 68500.00)
    max = Person("Maximus Kael", 28, 45200)
    print(lara, max)
