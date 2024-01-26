FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /url_app
COPY url_app ./url_app
COPY tests ./tests
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "-m", "url_app.main"]