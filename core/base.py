from abc import ABCMeta, abstractproperty

from persistence import InMemory


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


class ModelRestrictionError(Exception):
    """ Specific Exception class for model definition checks """

    def __init__(self, msg):
        self.msg = msg
        pass
