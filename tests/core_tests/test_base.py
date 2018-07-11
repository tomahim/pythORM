import unittest

from core.base import Base, ModelRestrictionError, Column, ColumnType


class ModelExample(Base):
    """ Class used for tests """
    model_name = 'example'
    columns = [
        Column('name', ColumnType.STRING)
    ]

    def __init__(self, **kwargs):
        super(ModelExample, self).__init__(**kwargs)
        self._name = kwargs.get('name')

    @property
    def name(self):
        return self._name


class TestBase(unittest.TestCase):

    def setUp(self):
        print('In method ' + self._testMethodName)

    def test_init_should_raise_exception_on_column_name_not_found(self):
        """ Attempt to create a model object with an unknown column name should raise exception """
        with self.assertRaises(ModelRestrictionError) as context:
            example = ModelExample(title='Test')
        self.assertIsInstance(context.exception, ModelRestrictionError)

    def test_init_should_raise_exception_on_column_type_incorrect(self):
        """ Attempt to set a model value with the wrong type should raise exception"""
        with self.assertRaises(ModelRestrictionError) as context:
            example = ModelExample(name=15)
        self.assertIsInstance(context.exception, ModelRestrictionError)

    def test_init_should_create_instance_variable(self):
        example = ModelExample(name='name val')
        self.assertEqual(example.name, 'name val')
