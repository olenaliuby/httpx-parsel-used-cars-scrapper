import asyncio
import logging

from sqlalchemy import select

from logger import setup_logging
from database.models import Car, PhoneNumber
from database.database import SessionLocal, init_db
from autoria_scraper.items import CarItem
from autoria_scraper.scraper import UsedCarScraper
from sqlalchemy.ext.asyncio import AsyncSession

setup_logging()


async def insert_or_update_car_data(
    car_item: CarItem, db_session: AsyncSession
) -> None:
    result = await db_session.execute(
        select(Car).where(Car.url == car_item.url)  # type: ignore
    )
    existing_car = result.scalars().first()

    if existing_car:
        existing_car.title = car_item.title
        existing_car.price_usd = car_item.price_usd
        existing_car.odometer = car_item.odometer
        existing_car.username = car_item.username
        existing_car.image_url = car_item.image_url
        existing_car.images_count = car_item.images_count
        existing_car.car_number = car_item.car_number
        existing_car.car_vin = car_item.car_vin
        existing_car.datetime_found = car_item.datetime_found
        logging.info(f"Updated car: {car_item.url}")
    else:
        existing_car = Car(
            url=car_item.url,
            title=car_item.title,
            price_usd=car_item.price_usd,
            odometer=car_item.odometer,
            username=car_item.username,
            image_url=car_item.image_url,
            images_count=car_item.images_count,
            car_number=car_item.car_number,
            car_vin=car_item.car_vin,
            datetime_found=car_item.datetime_found,
        )
        db_session.add(existing_car)
        logging.info(f"Inserted new car: {car_item.url}")

        for phone_item in car_item.phone_numbers:
            new_phone_number = PhoneNumber(
                phone_number=phone_item.phone_number, car_id=existing_car.id
            )
            db_session.add(new_phone_number)

    await db_session.commit()


async def main() -> None:
    await init_db()

    scraper = UsedCarScraper()
    async for car in scraper.scrape():
        logging.info(f"Crawled car: {car}")

        async with SessionLocal() as db_session:
            try:
                await insert_or_update_car_data(car, db_session)
            except Exception as e:
                logging.error(f"Failed to insert data for {car.url}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
