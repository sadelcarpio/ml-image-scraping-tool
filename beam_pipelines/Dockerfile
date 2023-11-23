FROM tensorflow/tensorflow
LABEL authors="sergio.delcarpio"

WORKDIR beam_pipelines/

COPY tests ./tests
COPY pipelines ./pipelines
COPY requirements.txt .
ENV GOOGLE_APPLICATION_CREDENTIALS /beam_pipelines/service_account.json


RUN grep -v "tensorflow" requirements.txt | xargs pip install
CMD ["python", "-m", "pipelines.to_tfrecord"]
