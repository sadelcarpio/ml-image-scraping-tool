import os
from datetime import datetime

import apache_beam as beam

from to_tfrecord.image_dofns import DecodeFromTextDoFn, ReadImagesDoFn, ImageToTfExampleDoFn


class ToTFRecordPipeline(beam.PTransform):
    def __init__(self, images_bucket, labels_bucket, tfrecord_bucket):
        super().__init__()
        self.images_bucket = images_bucket
        self.labels_bucket = labels_bucket
        self.tfrecord_bucket = tfrecord_bucket

    def expand(self, p):
        return (
                p
                | beam.io.ReadFromText(f'gs://{self.labels_bucket}/data_labeled.csv', skip_header_lines=1)
                | "Get path from gs filename" >> beam.ParDo(DecodeFromTextDoFn())
                | "Read images from paths" >> beam.ParDo(ReadImagesDoFn(bucket_name=self.images_bucket))
                | "Convert image bytes to TFRecord" >> beam.ParDo(ImageToTfExampleDoFn())
                | beam.Map(lambda x: x.SerializeToString())
                | beam.io.tfrecordio.WriteToTFRecord(file_path_prefix=f'gs://{self.tfrecord_bucket}/'
                                                                      f'{datetime.now().strftime("%d-%m-%Y")}/images',
                                                     shard_name_template='-SSSSS-of-NNNNN.tfrecord')
        )


def run_pipeline():
    with beam.Pipeline() as p:
        (
                p
                | ToTFRecordPipeline(os.environ["IMAGES_BUCKET_NAME"],
                                     os.environ["LABELS_BUCKET"],
                                     os.environ["TFRECORD_BUCKET"])
        )


if __name__ == "__main__":
    run_pipeline()
