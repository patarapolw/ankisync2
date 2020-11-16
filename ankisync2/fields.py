import json

import peewee as pv

from .util import DataclassJSONEncoder


class ArrayField(pv.TextField):
    separator = " "

    def db_value(self, value):
        return self.separator.join(value)

    def python_value(self, value):
        return value.strip().split(self.separator)


class X1fField(pv.TextField):
    separator = "\x1f"

    def db_value(self, value):
        return self.separator.join(value)

    def python_value(self, value):
        return value.strip().split(self.separator)


class JSONField(pv.TextField):
    def db_value(self, value):
        if value:
            return json.dumps(value, cls=DataclassJSONEncoder)

    def python_value(self, value):
        if value:
            return json.loads(value)
