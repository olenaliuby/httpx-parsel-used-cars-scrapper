from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    title = Column(String)
    price_usd = Column(Float)
    odometer = Column(Integer)
    username = Column(String)
    phone_numbers = relationship("PhoneNumber", back_populates="car")
    image_url = Column(String)
    images_count = Column(Integer)
    car_number = Column(String)
    car_vin = Column(String)
    datetime_found = Column(String)


class PhoneNumber(Base):
    __tablename__ = "phone_numbers"
    id = Column(Integer, primary_key=True)
    phone_number = Column(String)
    car_id = Column(Integer, ForeignKey("cars.id"))
    car = relationship("Car", back_populates="phone_numbers")
