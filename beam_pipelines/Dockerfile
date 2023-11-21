FROM tensorflow/tensorflow
LABEL authors="sergio.delcarpio"

WORKDIR beam_pipelines/

COPY tests ./tests
COPY requirements.txt .
COPY service_account.json .
ENV GOOGLE_APPLICATION_CREDENTIALS /beam_pipelines/service_account.json


RUN pip install -r requirements.txt
CMD ["python", "-m", "pipelines.to_tfrecord"]
