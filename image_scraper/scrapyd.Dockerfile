# Use an official Python runtime as a parent image
FROM python:3.10
LABEL authors="sadelcarpio"

# Install Chrome
RUN apt-get update && apt-get install -y \
  chromium \
  libnss3 \
  fontconfig \
  && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip \
  && unzip chromedriver_linux64.zip -d /usr/bin \
  && chmod +x /usr/bin/chromedriver \
  && rm chromedriver_linux64.zip

COPY scrapyd.conf /etc/scrapyd/scrapyd.conf
COPY requirements.txt .

RUN pip install -r requirements.txt

# Expost default Scrapyd port 6800
EXPOSE 6800

# Start Scrapyd server when container is run
CMD ["scrapyd"]