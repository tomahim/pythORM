from datetime import datetime

from utils.utils import enum

ColumnType = enum('STRING', 'DATETIME')


class Column:
    """ The Attribute class is used to register the model attributes
        The definition includes column name and the type of data
     """

    def __init__(self, column_name, column_type):
        self.column_name = column_name
        self.column_type = column_type
        pass

    def is_correct_value(self, value):
        """ Determines if the value match the defined Column type
            @return: boolean
        """
        if self.column_type == ColumnType.STRING:
            return isinstance(value, basestring)
        elif self.column_type == ColumnType.DATETIME:
            return type(value) is datetime


def get_model_columns(model):
    """ Inspect model object to get the defined Column objects
    @return: a dictionary with column names and attr
    """
    all_class_attributes = [getattr(model, attr_name) for attr_name in dir(model)]
    columns = [attr for attr in all_class_attributes if isinstance(attr, Column)]
    return dict(zip(map(lambda x: x.column_name, columns), columns))