import argparse
import os
from datetime import datetime

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

from to_tfrecord.image_dofns import DecodeFromTextDoFn, ReadImagesDoFn, ImageToTfExampleDoFn


class ToTFRecordPipeline(beam.PTransform):
    def __init__(self, images_bucket, labels_bucket, tfrecord_bucket, project):
        super().__init__()
        self.images_bucket = images_bucket
        self.labels_bucket = labels_bucket
        self.tfrecord_bucket = tfrecord_bucket
        self.project = project
        self.current_date = datetime.today().strftime("%Y-%m-%d")

    def expand(self, p):
        return (
                p
                | beam.io.ReadFromText(f'gs://{self.labels_bucket}/{self.project}/labels-{self.current_date}.csv',
                                       skip_header_lines=1)
                | "Get path from gs filename" >> beam.ParDo(DecodeFromTextDoFn())
                | "Read images from paths" >> beam.ParDo(ReadImagesDoFn(bucket_name=self.images_bucket))
                | "Convert image bytes to TFRecord" >> beam.ParDo(ImageToTfExampleDoFn())
                | beam.Map(lambda x: x.SerializeToString())
                | beam.io.tfrecordio.WriteToTFRecord(file_path_prefix=f'gs://{self.tfrecord_bucket}/'
                                                                      f'{datetime.now().strftime("%d-%m-%Y")}/images',
                                                     shard_name_template='-SSSSS-of-NNNNN.tfrecord')
        )


def run_pipeline():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--project',
        required=True,
        help='Project to read labels from.')

    known_args, pipeline_args = parser.parse_known_args()

    pipeline_options = PipelineOptions(pipeline_args)

    with beam.Pipeline(options=pipeline_options) as p:
        (
                p
                | ToTFRecordPipeline(images_bucket=os.environ["IMAGES_BUCKET_NAME"],
                                     labels_bucket=os.environ["LABELS_BUCKET"],
                                     tfrecord_bucket=os.environ["TFRECORD_BUCKET"],
                                     project=known_args.project)
        )


if __name__ == "__main__":
    run_pipeline()
