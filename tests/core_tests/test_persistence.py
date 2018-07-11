import unittest

from core.base import Base, Column, ColumnType
from core.persistence import InMemory, get_primary_key_column


class ModelExample(Base):
    columns = [
        Column('id', ColumnType.STRING, primary_key=True),
        Column('name', ColumnType.STRING)
    ]

    def __init__(self, name):
        self._id = None
        self._name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name


class TestPersistence(unittest.TestCase):
    mock_model = None
    existing_id = None
    db = InMemory()

    def setUp(self):
        print('In method ' + self._testMethodName)

    def init_db(self, with_data):
        self.db.store = dict()
        if with_data:
            mock_example = ModelExample(name='test')
            mock_example.id = '1'
            self.mock_model = mock_example
            self.db.store.update({'ModelExample': [mock_example]})
            self.existing_id = mock_example.id

    def init_multiple_data(self):
        self.db.store = dict()
        mock_example = ModelExample(name='test1')
        mock_example.id = '1'

        mock_example2 = ModelExample(name='duplicate')
        mock_example2.id = '2'

        mock_example3 = ModelExample(name='duplicate')
        mock_example3.id = '3'
        self.db.store.update({'ModelExample': [mock_example, mock_example2, mock_example3]})

    def test_in_memory_upsert_without_existing_data(self):
        # given
        self.init_db(with_data=False)

        new_model = ModelExample(name='test 2')

        # when
        result = self.db.upsert(new_model)

        # then
        self.assertIsNotNone(result.id)
        self.assertEqual(len(self.db.store.get('ModelExample')), 1)
        [entry] = self.db.store.get('ModelExample')
        self.assertEqual(entry.name, 'test 2')

    def test_in_memory_upsert_with_existing_data(self):
        # given
        self.init_db(with_data=True)
        mock_model = ModelExample(name='test2')

        # when
        result = self.db.upsert(mock_model)

        # then
        self.assertIsNotNone(result.id)
        self.assertEqual(len(self.db.store.get('ModelExample')), 2)

    def test_in_memory_find_by_id_should_pass(self):
        # given
        self.init_db(with_data=True)

        # when
        result = self.db.find_by_id(self.mock_model, self.existing_id)

        # then
        self.assertIsNotNone(result)

    def test_in_memory_find_all_should_pass(self):
        # given
        self.init_db(with_data=True)

        # when
        results = self.db.find_all(ModelExample)

        # then
        self.assertEqual(len(self.db.store.get('ModelExample')), 1)

    def test_in_memory_find_one_by_should_pass(self):
        # given
        self.init_db(with_data=True)

        # when
        result = self.db.find_one_by(ModelExample, 'name', 'test')

        # then
        self.assertEqual(result.id, '1')
        self.assertEqual(result.name, 'test')

    def test_in_memory_find_one_by_should_return_none(self):
        # given
        self.init_db(with_data=True)

        # when
        result = self.db.find_one_by(ModelExample, 'name', 'no existing')

        # then
        self.assertIsNone(result)

    def test_in_memory_find_list_by_should_pass(self):
        # given
        self.init_multiple_data()

        # when
        results = self.db.find_list_by(ModelExample, 'name', 'duplicate')

        # then
        self.assertEqual(len(results), 2)

    def test_in_memory_delete(self):
        # when
        self.init_db(with_data=True)
        self.db.delete(self.mock_model)

        # then
        self.assertEqual(len(self.db.store.get('ModelExample')), 0)

    def test_get_primary_column_should_retrieve_id(self):
        col = get_primary_key_column(ModelExample(name='test'))
        self.assertEqual(col.column_name, 'id')
