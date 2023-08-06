from collections import defaultdict
from datetime import datetime

from dateutil.parser import isoparse


class DistinguishedName:

    def __init__(self, s=None, **kwargs):
        self.relative_names = defaultdict(list)
        if s is not None:
            if len(kwargs) > 0:
                raise ValueError("specify a string or keyword args, not both")
            self.s = s
            for k, v in [tuple(rdn.split("=")) for rdn in s.split(",")]:
                self.relative_names[k.lower()].append(v)
        elif len(kwargs) > 0:
            self.s = ""
            for k, v in kwargs.items():
                self.s = (self.s + "," if len(self.s) > 0 else self.s) + k + "=" + str(v)
                self.relative_names[k.lower()].append(v)

    def keys(self):
        return self.relative_names.keys()

    def items(self):
        return [(k, self[k]) for k in self.relative_names.keys()]

    def __contains__(self, relative_name):
        return relative_name.lower() in self.relative_names

    def __getitem__(self, relative_name):
        name = self.relative_names[relative_name.lower()]
        if len(name) == 1:
            return name[0]
        return tuple(name)

    def __str__(self):
        return self.s

    def __repr__(self):
        return f"DN'{self.s}'"

    def __eq__(self, other):
        if not isinstance(other, DistinguishedName):
            return False
        return self.s.lower() == other.s.lower()

    def __hash__(self):
        return self.s.lower().__hash__()


class Attribute:

    def __init__(self, name, py_type: type = str, multivalued=False):
        self.name = name
        self.py_type = py_type
        self.multivalued = multivalued

    def _coerce(self, v):
        if self.py_type is bool:
            if v.lower() == "true":
                return True
            if v.lower() == "false":
                return False
            raise ValueError(f"cannot coerce `{v}` to a boolean")
        elif self.py_type is datetime:
            return isoparse(v)

        return self.py_type(v)

    def transform(self, value):
        value = [self._coerce(v) for v in value]
        if not self.multivalued:
            return value[0]
        return value


class ObjectClass:

    def __init__(self, name, *attributes: Attribute):
        self.name = name
        self.attributes = {at.name: at for at in attributes}

    def keys(self):
        return self.attributes.keys()

    def items(self):
        return self.attributes.items()

    def __contains__(self, name):
        return name in self.attributes

    def __getitem__(self, name) -> Attribute:
        return self.attributes.get(name)


class Schema:

    def __init__(self, *object_types: ObjectClass):
        self.object_classes = {ot.name: ot for ot in object_types}


