FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR labeling_app
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app ./app
COPY tests ./tests

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "4000"]