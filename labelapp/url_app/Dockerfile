FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY src ./src
COPY tests ./tests
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "-m", "src.main"]