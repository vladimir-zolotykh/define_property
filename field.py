#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Property:
    def __init__(self, fget, fset, fdel):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel

    def __get__(self, instance, owner):
        return self.fget(instance)

    def __set__(self, instance, value):
        return self.fset(instance, value)

    def __delete__(self, instance):
        self.fdel(instance)


class MetaProperty(type):
    def __new__(mcls, clsname, bases, clsdict):
        if "_fields" in clsdict:
            fields = clsdict["_fields"]
        else:
            for base in bases:
                if hasattr(base, "_fields"):
                    fields = getattr(base, "_fields")
                    break
            else:
                raise TypeError(f"{clsname} must define _fields or inherit it")

        for name in fields:

            def make_property(name):
                def getter(self):
                    return getattr(self, name)

                def setter(self, val):
                    setattr(self, name, val)

                def deleter(self):
                    delattr(self, name)

                return Property(getter, setter, deleter)

            clsdict[name] = make_property(f"_{name}")

        def __init__(self, *args, **kwargs):
            for k, v in zip(fields, args):
                self.__dict__[f"_{k}"] = v

        clsdict["__init__"] = __init__

        def __repr__(self):
            key_val_pairs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
            return f"{self.__class__.__name__}({key_val_pairs})"

        clsdict["__repr__"] = __repr__
        return super().__new__(mcls, clsname, bases, clsdict)


class SuperPerson(metaclass=MetaProperty):
    _fields = ["name", "age", "salary"]


class Person(SuperPerson):
    pass


if __name__ == "__main__":
    lara = Person("Elara Vance", 34, 68500.00)
    max = Person("Maximus Kael", 28, 45200)
    print(lara, max)
