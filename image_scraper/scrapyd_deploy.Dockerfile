# Use an official Python runtime as a parent image
FROM python:3.10
LABEL authors="sadelcarpio"

WORKDIR src/

COPY image_scraper ./image_scraper
COPY tests ./tests
COPY requirements.txt /src
COPY scrapy.cfg /src

# Install requirements and add module to pythonpath
RUN pip install -r requirements.txt

# Start Scrapyd server when container is run
CMD ["scrapyd-deploy", "docker"]