from sqlalchemy import Column, Integer, String, Date, Time, ARRAY
from sqlalchemy.ext.declarative import declarative_base

# Create a Base for SQLalchemy
Base = declarative_base()

# Create the events table with columns


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(String)
    date = Column(Date)
    time = Column(Time)
    location = Column(String)
    title = Column(String)
    artists = Column(ARRAY(String))
    works = Column(ARRAY(String))
    image_link = Column(String)
