import unittest

from mock import mock

from core.base import Base, ModelRestrictionError
from core.column import Column, ColumnType


class ModelExample(Base):
    """ Class used for tests """
    model_name = 'example'
    name = Column('name', ColumnType.STRING)


def mock_get_model_columns():
    """ Mock for core.column.get_model_columns """
    return {
        'name': Column('name', ColumnType.STRING)
    }


class TestBase(unittest.TestCase):

    @mock.patch('core.column.get_model_columns', mock_get_model_columns)
    def test_init_should_raise_exception_on_column_name_not_found(self):
        """ Attempt to create a model object with an unknown column name should raise exception """
        with self.assertRaises(ModelRestrictionError) as context:
            example = ModelExample(title='Test')
        self.assertIsInstance(context.exception, ModelRestrictionError)

    @mock.patch('core.column.get_model_columns', mock_get_model_columns)
    def test_init_should_raise_exception_on_column_name_not_found(self):
        """ Attempt to set a model value with the wrong type should raise exception"""
        with self.assertRaises(ModelRestrictionError) as context:
            example = ModelExample(name=15)
        self.assertIsInstance(context.exception, ModelRestrictionError)

    @mock.patch('core.column.get_model_columns', mock_get_model_columns)
    def test_init_should_create_instance_variable(self):
        example = ModelExample(name='name val')
        self.assertEqual(example.name, 'name val')
