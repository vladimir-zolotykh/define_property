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
    pass


class SuperPerson(metaclass=MetaProperty):
    _fields = ["name", "age", "salary"]


class Person:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_name(self, val):
        self._name = val

    def del_name(self):
        del self._name

    name = Property(get_name, set_name, del_name)

    def __repr__(self):
        key_val_pairs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({key_val_pairs})"


if __name__ == "__main__":
    lara = Person("Elara Vance")
    print(lara.name)
    lara.name = "Elara Kael"
    print(lara.name)
    print(lara)
