import unittest

from core.base import Base
from core.column import Column, ColumnType


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
    db = None

    def setUp(self):
        mock_example = ModelExample(name='test')
        mock_example.persist()

        self.mock_model = mock_example
        self.existing_id = mock_example.id
        self.db = mock_example.db

    def test_in_memory_upsert_without_existing_data(self):
        # given
        new_model = ModelExample(name='test 2')

        # when
        result = self.db.upsert(new_model)

        # then
        self.assertIsNotNone(result.id)
        self.assertEqual(len(self.db.store.get('ModelExample')), 1)
        [entry] = self.db.store.get('ModelExample')
        self.assertEqual(entry.name, 'test 2')

    def test_in_memory_find_by_id_should_pass(self):
        # when
        result = self.db.find_by_id(self.mock_model, self.mock_model.id)

        # then
        self.assertIsNotNone(result)

    # @mock.patch("core.persistence.InMemory.store", dict(
    #     MockExample=[mock_model]
    # ))
    # def test_in_memory_upsert_with_existing_data(self):
    #     # when
    #     entry = db.store.get('ModelExample')
    #     print('heeee')
    #     print(entry.id)
    #     result = db.upsert(mock_model)
    #
    #     # then
    #     self.assertIsNotNone(result.id)
    #     self.assertEqual(len(db.store.get('ModelExample')), 1)
    #     [entry] = db.store.get('ModelExample')
    #     print(entry.id)
    #     self.assertEqual(entry.name, 'test 2')

    def test_in_memory_delete(self):
        # when
        self.db.delete(self.mock_model)

        # then
        self.assertEqual(len(self.db.store.get('ModelExample')), 0)
