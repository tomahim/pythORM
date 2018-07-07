from abc import ABCMeta, abstractproperty

from core.column import Column, get_model_columns


class Base(object):
    """ The Base abstract class """
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        columns = get_model_columns(self)

        # dynamically define class instance variables with columns definition check
        for column_name in kwargs:
            column_value = kwargs[column_name]

            if column_name not in columns:
                raise ModelRestrictionError('Unknown column ' + column_name)

            if not columns[column_name].is_correct_value(column_value):
                raise ModelRestrictionError('Value type not allowed for ' + column_name)

            setattr(self, column_name, kwargs[column_name])

    @abstractproperty
    def model_name(self):
        """ String identifier for a model """
        pass


class ModelRestrictionError(Exception):
    """ Specific Exception class for model definition checks """

    def __init__(self, msg):
        self.msg = msg
        pass
