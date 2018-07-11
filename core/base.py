from abc import ABCMeta, abstractproperty
from persistence import InMemory
from datetime import datetime
from utils.utils import enum


class Base(object):
    __metaclass__ = ABCMeta
    """ The Base class
        Every model should inherit from this class
        It gives the ability to define a model with columns and type checking
    """

    db = InMemory()

    def __init__(self, **kwargs):
        # Check columns definition
        for column_name in kwargs:
            column = next(iter([col for col in self.columns if col.column_name == column_name]), None)
            column_value = kwargs.get(column_name)

            if not column:
                raise ModelRestrictionError('Unknown column ' + column_name)

            if not column.is_correct_value_type(column_value):
                raise ModelRestrictionError('Value type not allowed for ' + column_name)

    @abstractproperty
    def columns(self):
        """ Columns list defining the model """
        return []

    def persist(self):
        return self.db.upsert(self)

    def delete(self):
        return self.db.delete(self)


ColumnType = enum('STRING', 'DATETIME', 'NUMERIC')


class Column:
    """ The Attribute class is used to register the model attributes
        The definition includes column name and the type of data
     """

    def __init__(self, column_name, column_type, primary_key=False, foreign_key=False):
        self.column_name = column_name
        self.column_type = column_type
        self.primary_key = primary_key
        # FIXME: foreign_key is not used for now
        # TODO: use foreign_key for joining models and check foreign key constraint on persistence
        self.foreign_key = foreign_key
        pass

    def is_correct_value_type(self, value):
        """ Determines if the value match the defined Column type
            @return: boolean
        """
        if self.column_type == ColumnType.STRING:
            return isinstance(value, basestring)
        elif self.column_type == ColumnType.DATETIME:
            return type(value) is datetime
        elif self.column_type == ColumnType.NUMERIC:
            return type(value)


class ModelRestrictionError(Exception):
    """ Specific Exception class for model definition checks """

    def __init__(self, msg):
        self.msg = msg
        pass
