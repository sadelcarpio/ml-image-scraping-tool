FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

EXPOSE 5000

RUN pip install -r requirements.txt

COPY update_last_processed ./dag_info
COPY tests ./tests

CMD ["uvicorn", "update_last_processed.main:app", "--host", "0.0.0.0", "--port", "5000"]