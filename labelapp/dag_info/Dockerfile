FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY dag_info ./dag_info
COPY tests ./tests
COPY requirements.txt .

EXPOSE 3000

RUN pip install -r requirements.txt

CMD ["uvicorn", "dag_info.main:app", "--host", "0.0.0.0", "--port", "3000"]