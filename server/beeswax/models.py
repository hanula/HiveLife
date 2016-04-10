from datetime import datetime
from sqlalchemy import (
    orm,
    Column,
    Index,
    ForeignKey,
    Integer,
    Float,
    String,
    Text,
    DateTime,
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))


class ModelBase(object):
    """
    Base class for all models.

    Provides helpers to query and manage objects in the session.
    """
    query = DBSession.query_property()

    def save(self):
        DBSession.add(self)

    @classmethod
    def get_by(cls, **attrs):
        return cls.query.filter_by(**attrs).first()

    @classmethod
    def get_or_create(cls, **attrs):
        obj = cls.get_by(**attrs)
        if not obj:
            obj = cls(**attrs)
            DBSession.add(obj)
        return obj

Base = declarative_base(cls=ModelBase)


class Location(Base):
    """
    Beehives location/farm.
    """
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True, index=True)
    description = Column(String(128), unique=True, index=True)


class Hive(Base):
    """
    A hive that contains sensors.
    """
    __tablename__ = 'hives'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    name = Column(String(32), index=True)

    location = orm.relationship(Location)


class Sensor(Base):
    """
    Sensor is a device in the hive providing a measurements of given type.
    """
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True)
    hive_id = Column(Integer, ForeignKey('hives.id'))
    name = Column(String(32), index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    type_name = Column(String(32))

    hive = orm.relationship(Hive)

    @property
    def types(self):
        return [m.name for m in self.measurements.group_by(Measurement.name)]


class Measurement(Base):
    """
    Sensor readings of float-type values.
    """
    __tablename__ = 'measurements'
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey('sensors.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    value = Column(Float)

    sensor = orm.relationship(Sensor, backref=orm.backref('measurements',
                                                          lazy='dynamic'))
