"""Scrape car details from auto.ria.com"""

import json
import logging

from logger import setup_logging
from typing import Generator

import httpx
import asyncio
from parsel import Selector
from autoria_scraper.parser import UsedCarParser, PhoneNumberParser
from autoria_scraper.items import CarItem

setup_logging()


class UsedCarScraper:
    def __init__(self):
        self.base_url = "https://auto.ria.com/uk/car/used/"
        self.allowed_domains = ["auto.ria.com"]

    async def fetch(self, url: str, timeout: float = 10.0) -> str:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=timeout)
                response.raise_for_status()
                return response.text
            except httpx.RequestError as exc:
                logging.error(
                    f"An error occurred while requesting {exc.request.url!r}."
                )
            except httpx.HTTPStatusError as exc:
                logging.error(
                    f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
                )

    async def scrape_car_details(self, car_url: str) -> CarItem:
        html = await self.fetch(car_url)
        car_item = UsedCarParser().parse_car_details(html, car_url)
        return car_item

    async def fetch_phone_numbers(self, car_item: CarItem) -> CarItem:
        phone_numbers_html = await self.fetch(car_item.url)
        phone_info = PhoneNumberParser.extract_phone_number_info(
            Selector(text=phone_numbers_html)
        )

        if phone_info:
            data_hash, data_expires, data_auto_id = phone_info
            phone_numbers_url = PhoneNumberParser.get_phone_numbers_url(
                data_hash, data_auto_id, data_expires
            )
            phone_numbers_response = await self.fetch(phone_numbers_url)

            if phone_numbers_response:
                try:
                    phone_numbers_data = json.loads(phone_numbers_response)
                    car_item.phone_numbers = PhoneNumberParser.parse_phone_numbers(
                        phone_numbers_data
                    )
                    logging.info(f"Fetched phone numbers for {car_item.url}")
                except json.JSONDecodeError:
                    logging.error("Error parsing JSON from the phone numbers response")
                    car_item.phone_numbers = []
            else:
                logging.error("Received empty response for phone numbers")
                car_item.phone_numbers = []

        return car_item

    async def scrape(self) -> Generator[CarItem, None, None]:
        first_page = await self.fetch(self.base_url)
        total_pages = self.get_total_pages(first_page)

        for page_number in range(1, total_pages + 1):
            page_url = f"{self.base_url}?page={page_number}"
            logging.info(f"Scraping page {page_number}/{total_pages}")
            page_html = await self.fetch(page_url)
            car_urls = self.extract_car_urls(page_html)
            for car_url in car_urls:
                car_item = await self.scrape_car_details(car_url)
                car_item = await self.fetch_phone_numbers(car_item)
                yield car_item

    @staticmethod
    def get_total_pages(html: str) -> int:
        selector = Selector(text=html)
        total_pages_text = selector.css(
            "#pagination > nav > span:nth-child(8) > a::text"
        ).get()
        return int(total_pages_text.replace(" ", "")) if total_pages_text else 1

    @staticmethod
    def extract_car_urls(html: str) -> list[str]:
        selector = Selector(text=html)
        return selector.css(
            "#searchResults section.ticket-item div.content-bar a.m-link-ticket::attr(href)"
        ).getall()


async def main() -> None:
    scraper = UsedCarScraper()
    async for car in scraper.scrape():
        logging.info(f"Crawled car: {car}")


if __name__ == "__main__":
    asyncio.run(main())
