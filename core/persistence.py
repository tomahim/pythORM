import uuid
from abc import ABCMeta, abstractmethod

from core.column import get_primary_key_column


class DB(object):
    """ The DB abstract class """
    __metaclass__ = ABCMeta

    @abstractmethod
    def find_by_id(self, model, obj_id):
        pass

    @abstractmethod
    def find_list_by(self, model, column_name, column_value):
        pass

    @abstractmethod
    def find_one_by(self, model, column_name, column_value):
        pass

    @abstractmethod
    def upsert(self, model):
        pass

    @abstractmethod
    def delete(self, model):
        pass


class InMemory(DB):
    """ Class implementing an in memory database with CRUD operations """

    # dictionary containing all the model data (with Base.model_name as keys)
    store = dict()

    def find_one_by(self, model, column_name, column_value):
        model_name = model.get_model_name()
        all_items = self.store.get(model_name)
        if not all_items:
            return None
        return next(iter([item for item in all_items if getattr(item, column_name) == column_value]), None)

    def find_by_id(self, model, obj_id):
        pk_column = get_primary_key_column(model)
        return self.find_one_by(model, pk_column.column_name, obj_id)

    def find_list_by(self, model, column_name, column_value):
        model_name = model.get_model_name()
        all_items = self.store.get(model_name)
        if not all_items:
            return None
        return [item for item in all_items if getattr(item, column_name) == column_value]

    def upsert(self, model):
        model_name = model.get_model_name()
        pk_column = get_primary_key_column(model)
        pk_name = pk_column.column_name
        obj_id = getattr(model, pk_column.column_name)
        # update if a primary key is already defined
        if obj_id:
            existing = self.find_by_id(model, obj_id)
            if existing:
                map(lambda item: model if getattr(item, pk_column.column_name) == obj_id else item,
                    self.store.get(model_name))
            else:
                raise DbException('Object with unknown id')
        else:
            # insert
            setattr(model, pk_name, self.__generate_id())
            # if no object of this model stored before, we initialize a list
            if model_name not in self.store:
                self.store.update({model_name: [model]})
            else:
                self.store.update({
                    model_name: self.store.get(model_name) + [model]
                })
        return model

    def delete(self, model):
        model_name = model.get_model_name()
        pk_column = get_primary_key_column(model)
        obj_id = getattr(model, pk_column.column_name)
        all_items = self.store.get(model_name)
        if all_items:
            self.store.update({
                model_name: [item for item in all_items if getattr(item, pk_column.column_name) != obj_id]
            })

    def __generate_id(self):
        return uuid.uuid4()



class DbException(Exception):
    def __init__(self, msg):
        self.msg = msg