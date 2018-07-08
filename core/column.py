from datetime import datetime

from utils.utils import enum

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


def get_primary_key_column(model):
    """ Get the primary key Column
    @return: The Column object
    """
    return next(iter([col for col in model.columns if col.primary_key]), None)
