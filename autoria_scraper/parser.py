"""Parser module for parsing the car details from the HTML page."""

import re
from datetime import datetime

from parsel import Selector
from autoria_scraper.items import CarItem, PhoneNumberItem


class UsedCarParser:
    def parse_car_details(self, html: str, url: str) -> CarItem:
        selector = Selector(text=html)

        car_item = CarItem(
            url=url,
            title=selector.css("h1.head::text").get(),
            price_usd=int(
                selector.css("div.price_value strong::text")
                .re_first(r"(\d+\s*\d+)")
                .replace(" ", "")
            ),
            odometer=self.get_odometer(selector),
            username=UsedCarParser.get_user_name(selector),
            image_url=selector.css(
                "#photosBlock div.photo-620x465 picture img::attr(src)"
            ).get(),
            images_count=UsedCarParser.get_images_count(selector),
            car_number=UsedCarParser.get_car_number(selector),
            car_vin=UsedCarParser.get_car_vin(selector),
            datetime_found=datetime.now().isoformat(),
        )

        return car_item

    @staticmethod
    def get_odometer(selector: Selector) -> int:
        """Get the odometer reading from the page."""
        odometer = selector.css("div.base-information span.size18::text").re_first(
            r"(\d+)"
        )
        if odometer:
            return int(odometer) * 1000
        return 0

    @staticmethod
    def get_user_name(selector: Selector) -> str | None:
        css_selectors = [
            "#userInfoBlock div.seller_info div.seller_info_name a::text",
            "#userInfoBlock div.seller_info.mb-15 div h4 a::text",
            "#userInfoBlock div.seller_info_area div h4 a::text",
            "#userInfoBlock div.seller_info div.seller_info_name::text",
        ]

        for css_selector in css_selectors:
            user_name = selector.css(css_selector).get()
            if user_name:
                return user_name.strip()

        return None

    @staticmethod
    def get_images_count(selector: Selector) -> int:
        """Get the number of images of the car from the page."""
        images_count_text = selector.css(
            "#photosBlock .preview-gallery.mhide .action_disp_all_block a.show-all::text"
        ).get()

        if images_count_text is None:
            images_count_text = selector.css(
                "#photosBlock div.gallery-order.carousel div.count-photo.left span span.dhide::text"
            ).get()

        if images_count_text and isinstance(images_count_text, str):
            match = re.search(r"\d+", images_count_text)
            if match:
                return int(match.group())

        return 0

    @staticmethod
    def get_car_number(selector: Selector) -> str | None:
        car_number = selector.css(
            "div.auto-wrap > main > div.m-padding > div.vin-checked.mb-15.full div.t-check > span.state-num::text"
        ).get()
        if car_number:
            return car_number.strip()

        return None

    @staticmethod
    def get_car_vin(selector: Selector) -> str | None:
        car_vin = selector.css(
            "div.auto-wrap > main > div.m-padding > div.vin-checked.mb-15.full  div.t-check > span.label-vin::text"
        ).get()
        if car_vin:
            return car_vin.strip()

        return None


class PhoneNumberParser:
    @staticmethod
    def extract_phone_number_info(selector: Selector) -> tuple[str, str, str]:
        script_tag = selector.css('[class^="js-user-secure"]')
        data_auto_id = selector.css("body::attr(data-auto-id)").get()
        data_hash = script_tag.xpath("@data-hash").get()
        data_expires = script_tag.xpath("@data-expires").get()

        return data_hash, data_expires, data_auto_id

    @staticmethod
    def get_phone_numbers_url(
        data_hash: str, data_auto_id: str, data_expires: str
    ) -> str:
        return f"https://auto.ria.com/users/phones/{data_auto_id}/?hash={data_hash}&expires={data_expires}"

    @staticmethod
    def parse_phone_numbers(response: dict) -> list[PhoneNumberItem]:
        if not response["phones"]:
            return []
        phone_numbers = [
            phone["phoneFormatted"] for phone in response.get("phones", [])
        ]
        return [PhoneNumberItem(phone_number=phone) for phone in phone_numbers]
