from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.database.logs_database import logging_base


# logging database
class Logs(logging_base):
    __tablename__ = 'logs'
    
    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime)
    user_id = Column(Integer)
    event_type_id = Column(Integer, ForeignKey('event_type.id'))
    space_type_id = Column(Integer, ForeignKey('space_type.id'))
    entity_id = Column(Integer)

    event_type = relationship('EventType', back_populates='logs')
    space_type = relationship('SpaceType', back_populates='logs')

class EventType(logging_base):
    __tablename__ = 'event_type'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    logs = relationship('Logs', back_populates='event_type')

class SpaceType(logging_base):
    __tablename__ = 'space_type'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    logs = relationship('Logs', back_populates='space_type')