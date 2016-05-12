import os
import sys

# SQLalchemy configuration
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Floorplan(Base):
    __tablename__ = 'floorplan'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(300), default='No description provided...')
    square_footage = Column(Integer, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'square_footage': self.square_footage,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
        }

class Unit(Base):
    __tablename__ = 'unit'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    status = Column(String(20), default='Vacant')
    description = Column(String(300), default='No description provided...')
    floorplan_id = Column(Integer, ForeignKey('floorplan.id'))
    floorplan = relationship(Floorplan)
    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'floorplan_id': self.square_footage,
        }
    

engine = create_engine('sqlite:///apartment-inventory.db')
Base.metadata.create_all(engine)
