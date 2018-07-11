import unittest

from datetime import datetime

from core.base import Base, Column, ColumnType


class ModelExample(Base):
    """ Class used for tests """
    model_name = 'example'
    columns = [
        Column('id', ColumnType.STRING, primary_key=True),
        Column('name', ColumnType.STRING),
        Column('creation_date', ColumnType.DATETIME)
    ]


class TestColumn(unittest.TestCase):

    def setUp(self):
        print('In method ' + self._testMethodName)

    def test_init_should_set_instance_variables(self):
        column = Column('custom_name', ColumnType.STRING)
        self.assertEqual(column.column_name, 'custom_name')
        self.assertEqual(column.column_type, ColumnType.STRING)

    def test_is_correct_value_string_should_return_false(self):
        # given
        column = Column('string_column', ColumnType.STRING)
        # when
        result = column.is_correct_value_type(15)
        # then
        self.assertFalse(result)

    def test_is_correct_value_string_should_return_true(self):
        # given
        column = Column('string_column', ColumnType.STRING)
        # when
        result = column.is_correct_value_type('test')
        # then
        self.assertTrue(result)

    def test_is_correct_value_datetime_should_return_false(self):
        # given
        column = Column('datetime_column', ColumnType.DATETIME)
        # when
        result = column.is_correct_value_type('test')
        # then
        self.assertFalse(result)

    def test_is_correct_value_datetime_should_return_true(self):
        # given
        column = Column('datetime_column', ColumnType.DATETIME)
        # when
        result = column.is_correct_value_type(datetime.now())
        # then
        self.assertTrue(result)