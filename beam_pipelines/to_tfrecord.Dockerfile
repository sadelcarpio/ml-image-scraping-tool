FROM tensorflow/tensorflow
LABEL authors="sergio.delcarpio"

WORKDIR /src

COPY tests /src/tests
COPY to_tfrecord /src/to_tfrecord
COPY requirements.txt .
ENV GOOGLE_APPLICATION_CREDENTIALS /beam_pipelines/service_account.json


RUN grep -v "tensorflow" requirements.txt | xargs pip install
CMD ["python", "-m", "to_tfrecord", "--runner=DirectRunner"]
