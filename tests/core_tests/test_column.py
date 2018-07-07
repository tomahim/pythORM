import unittest

from datetime import datetime

from core.base import Base
from core.column import Column, ColumnType, get_model_columns


class ModelExample(Base):
    """ Class used for tests """
    model_name = 'example'
    name = Column('name', ColumnType.STRING)
    creation_date = Column('creation_date', ColumnType.DATETIME)
    not_a_column = 'test'
    __private_variable = 'test2'

    def __init__(self):
        pass

    def some_method(self):
        pass

    @property
    def some_property(self):
        return None


class TestColumn(unittest.TestCase):

    def test_init_should_set_instance_variables(self):
        column = Column('custom_name', ColumnType.STRING)
        self.assertEqual(column.column_name, 'custom_name')
        self.assertEqual(column.column_type, ColumnType.STRING)

    def test_is_correct_value_string_should_return_false(self):
        # given
        column = Column('string_column', ColumnType.STRING)
        # when
        result = column.is_correct_value(15)
        # then
        self.assertFalse(result)

    def test_is_correct_value_string_should_return_true(self):
        # given
        column = Column('string_column', ColumnType.STRING)
        # when
        result = column.is_correct_value('test')
        # then
        self.assertTrue(result)

    def test_is_correct_value_datetime_should_return_false(self):
        # given
        column = Column('datetime_column', ColumnType.DATETIME)
        # when
        result = column.is_correct_value('test')
        # then
        self.assertFalse(result)

    def test_is_correct_value_datetime_should_return_true(self):
        # given
        column = Column('datetime_column', ColumnType.DATETIME)
        # when
        result = column.is_correct_value(datetime.now())
        # then
        self.assertTrue(result)

    def test_get_model_columns_should_retrieve_only_column_variables(self):
        columns = get_model_columns(ModelExample())
        self.assertEqual(len(columns), 2)
        self.assertTrue('name' in columns)
        self.assertTrue('creation_date' in columns)
