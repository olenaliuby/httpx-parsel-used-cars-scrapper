"""This module contains the dataclass for the car item."""
from dataclasses import dataclass


@dataclass
class CarItem:
    url: str
    title: str
    price_usd: float
    odometer: int
    username: str | None
    phone_number: str | None
    image_url: str
    images_count: int
    car_number: str | None
    car_vin: str | None
    datetime_found: str
