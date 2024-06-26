# Use an official Python runtime as a parent image
FROM python:3.10
LABEL authors="sadelcarpio"

# install google chrome, no need for chromedriver
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# set display port to avoid crash
ENV DISPLAY=:99

WORKDIR /src

COPY requirements.txt .

ENV GOOGLE_APPLICATION_CREDENTIALS /src/service_account.json
RUN pip install -r requirements.txt

COPY image_scraper /src/image_scraper
COPY tests /src/tests
COPY requirements.txt /src
COPY scrapy.cfg /src
