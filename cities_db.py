import sqlalchemy
from sqlalchemy import Column, INTEGER, TEXT, FLOAT, DATE
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Cities(Base):
    __tablename__ = "cities"
    __table_args__ = {'schema': 'cities'}

    name = Column(TEXT, nullable=False, primary_key=True, comment='City name')
    location = Column(TEXT, nullable=False, comment='City location')


class Weather(Base):
    __tablename__ = 'weather'
    __table_args__ = {'schema': 'cities'}

    city_id = Column(INTEGER, nullable=False, primary_key=True,
                     comment='City ID')
    city = Column(TEXT, nullable=False, comment='City name')
    temp_lo = Column(INTEGER, nullable=False, comment='Low temperature')
    temp_hi = Column(INTEGER, nullable=False, comment='High temperature')
    prcp = Column(FLOAT, nullable=False, comment='Precipitation')
    date = Column(DATE, nullable=False, comment='Date')


CITIES_ROWS = [
    {
        "name": "San Francisco",
        "location": "(-194.0, 53.0)"
    }
]

WEATHER_ROWS = [
    {
        "city_id": 1,
        "city": "San Francisco",
        "temp_lo": 46,
        "temp_hi": 50,
        "prcp": 0.25,
        "date": "1994-11-27"
    },
    {
        "city_id": 2,
        "city": "San Francisco",
        "temp_lo": 43,
        "temp_hi": 57,
        "prcp": 0.00,
        "date": "1994-11-29"
    }
]

CITY_ROWS = {
    Cities: CITIES_ROWS,
    Weather: WEATHER_ROWS
}
