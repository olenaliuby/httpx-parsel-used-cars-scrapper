from dataclasses import dataclass, field


@dataclass
class CarItem:
    url: str
    title: str
    price_usd: float
    odometer: int
    username: str | None
    image_url: str
    images_count: int
    car_number: str | None
    car_vin: str | None
    datetime_found: str
    phone_numbers: list["PhoneNumber"] = field(default_factory=list)


@dataclass
class PhoneNumber:
    phone_number: str
