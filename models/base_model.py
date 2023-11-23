#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models

Base = declarative_base()

class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if 'id' not in kwargs:
            self.id = str(uuid.uuid4())

        if 'created_at' not in kwargs:
            self.created_at = datetime.utcnow()

        if 'updated_at' not in kwargs:
            self.updated_at = datetime.utcnow()

        for key, value in kwargs.items():
            if key not in ['__class__', 'created_at', 'updated_at']:
                setattr(self, key, value)

    def save(self):
        """Updates updated_at with the current time when the instance is changed"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Converts the instance into a dictionary format"""
        dictionary = {key: value for key, value in self.__dict__.items() if key != '_sa_instance_state'}
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        dictionary['updated_at'] = self.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        return dictionary

    def delete(self):
        """Deletes the current instance from the storage"""
        models.storage.delete(self)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = self.__class__.__name__
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)
