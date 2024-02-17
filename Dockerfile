FROM python:3.10.7-slim-buster
LABEL maintainer="olena.liuby@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt

COPY . .
COPY dumps_script.sh /usr/local/bin/dumps_script.sh

RUN chmod +x /usr/local/bin/dumps_script.sh

RUN apt-get update && apt-get install -y postgresql-client

# Cron Jobs for running the dumps script
RUN apt-get install -y cron
RUN (crontab -l ; echo "0 * * * * /usr/local/bin/dumps_script.sh") | crontab -

# Command starts cron and keep the container running
CMD ["cron", "-f", "&"]