FROM python:3.10-slim
COPY --from=openjdk:8-jre-slim /usr/local/openjdk-8 /usr/local/openjdk-8
LABEL authors="sergio.delcarpio"

WORKDIR /src

ENV GOOGLE_APPLICATION_CREDENTIALS /src/service_account.json
ENV JAVA_HOME /usr/local/openjdk-8
RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-8/bin/java 1
RUN pip install apache-beam[gcp]

COPY service_account.json /src/service_account.json

ENTRYPOINT ["python", "-m", "upload_csv_labels", "--runner=DirectRunner"]
