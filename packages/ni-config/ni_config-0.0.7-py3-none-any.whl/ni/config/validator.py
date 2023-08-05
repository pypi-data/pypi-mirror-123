# coding: utf-8

from jsonschema import validate, ValidationError


class ParameterValidator(object):

    def __init__(self, parameter_schema: dict):
        self._parameter_schema = parameter_schema

    def validates(self, parameters: dict):
        res = True
        try:
            for parameter_name, parameter_value in parameters.items():
                if parameter_name in self._parameter_schema:
                    validate(instance=parameter_value, schema=self._parameter_schema[parameter_name])
                else:
                    res = False
                    break
        except ValidationError:
            res = False
        finally:
            return res

    def validate(self, parameter_name: str, parameter_value):
        res = True
        try:
            if parameter_name in self._parameter_schema:
                validate(instance=parameter_value, schema=self._parameter_schema[parameter_name])
            else:
                res = False
        except ValidationError:
            res = False
        finally:
            return res
