import os
import json
from datetime import datetime
from google.cloud import datastore

class Base(object):
    client = datastore.Client()
    datastore = datastore
    project = os.getenv('PROJECT_ID')

    @classmethod
    def kind(cls):
        if hasattr(cls, 'KIND'):
            return cls.KIND
        else:
            return cls.__name__

    @classmethod
    def key(cls, path):
        return cls.datastore.Key(
            cls.kind(),
            path,
            project=cls.project
        )

    @classmethod
    def query(cls, **kwargs):
        return cls.client.query(kind=cls.kind(), **kwargs)

    def __init__(self, key=None, entity=None, **kwargs):
        if entity:
            self.entity = entity
        elif key:
            entity = self.client.get(key)
            if entity:
                self.entity = entity
            else:
                self.entity = datastore.Entity(
                    key=key,
                    exclude_from_indexes=self.exclude_from_indexes,
                )
        else:
            self.entity = datastore.Entity(exclude_from_indexes=self.exclude_from_indexes)

        for k in kwargs:
            self.entity[k] = kwargs.get(k)

    def put(self, key=None):
        if key:
            self.entity.key = key
        elif self.entity.key is None:
            self.entity.key = datastore.Key(self.__class__.kind(), project=self.project)

        self.client.put(self.entity)

    def get(self, key, default=None):
        if key in self.entity:
            return self.entity[key]
        else:
            return default

    def __getitem__(self, key):
        return self.entity[key]

    def __setitem__(self, key, value):
        self.entity[key] = value

    def items(self):
        return self.entity.items()

    def to_dict(self):
        return dict(self.entity)

    @property
    def exclude_from_indexes(self):
        return []

class BaseJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, Base):
            return o.entity
        return super(BaseJSONEncoder, self).default(o)

