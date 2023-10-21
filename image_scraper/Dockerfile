# Use an official Python runtime as a parent image
FROM python:3.8
LABEL authors="sadelcarpio"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /src

# Install Scrapyd and scrapyd-client
RUN pip install scrapyd

# Add your project to the docker image
ADD . /src

# Expost default Scrapyd port 6800
EXPOSE 6800

# Start Scrapyd server when container is run
CMD ["scrapyd"]