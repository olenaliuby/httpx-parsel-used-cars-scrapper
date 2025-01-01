# Used Cars Scraper

## Project Overview

The Used Cars Scraper is an application designed to scrape and store data about used cars from the AutoRia platform.
This project utilizes `httpx` for making asynchronous HTTP requests and `parsel` for parsing HTML content. The scraped
data is stored in a PostgreSQL database. The application is structured to support efficient data handling and storage,
making it an ideal solution for aggregating large volumes of car data.

## Installation

Follow these steps to install and run the Used Cars Scraper:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/olenaliuby/httpx-parsel-used-cars-scrapper.git
   cd used-car-scrapping-autoria
   ```

2. **Environment Configuration**:
   Create a `.env` file in the root directory with the following content:
   ```plaintext
   POSTGRES_HOST=<your db hostname>
   POSTGRES_DB=<your db name>
   POSTGRES_USER=<your db username>
   POSTGRES_PASSWORD=<your db user password>
   BACKUP_TIME=12:00 # Time in 24-hour format
   ```

3.**Activate venv**:

   ```bash
   python -m venv venv
   source venv/bin/activate (Linux/Mac)
   venv\Scripts\activate (Windows)
   ``` 

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Build and Run with Docker**:
   ```bash
   docker-compose up --build
   ```

## Usage

To use the scraper:

1. **Access the app container**:
   ```bash
   docker ps
   docker exec -it <app_container_id> bash
   ```

2. **Run the scraper**:
   ```bash
   python run_scraper.py
   ```

## Key Features

- **Data Scraping**: Automated scraping of used car details from AutoRia using `httpx` and `parsel`.
- **Data Storage**: Efficient storage and management of scraped data in a PostgreSQL database.
- **API Access**: API endpoints to access and manage the scraped data.
- **Daily Backups**: Automated daily backups of the database at a specified time.

## Key Technologies Used

- **httpx**: A fully featured HTTP client for Python 3, which provides synchronous and asynchronous APIs.
- **parsel**: A library for extracting data from HTML and XML using XPath and CSS selectors.
- **PostgreSQL**: A powerful, open-source object-relational database system.
- **Docker**: A set of platform-as-a-service products that use OS-level virtualization to deliver software in packages
  called containers.

## Maintainer

- Olena Liuby ([olena.liuby@gmail.com])
