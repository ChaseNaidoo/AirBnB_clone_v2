#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
import shlex


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state",
                          cascade="all, delete, delete-orphan")

    @property
    def cities(self):
        all_instances = models.storage.all()
        city_instances = []
        result = []

        for key in all_instances:
            instance = key.replace('.', ' ')
            instance = shlex.split(instance)

            if instance[0] == 'City':
                city_instances.append(all_instances[key])

        for city in city_instances:
            if city.state_id == self.id:
                result.append(city)

        return result
