import os

import apache_beam as beam

from pipelines.to_tfrecord.image_dofns import DecodeFromTextDoFn, ReadImagesDoFn, ImageToTfExampleDoFn

IMAGES_BUCKET_NAME = os.environ["IMAGES_BUCKET_NAME"]

with beam.Pipeline() as p:

    pipeline = (
            p
            | beam.io.ReadFromText(f'gs://{os.environ["LABELS_BUCKET"]}/data_labeled.csv', skip_header_lines=1)
            | beam.ParDo(DecodeFromTextDoFn(bucket_name=IMAGES_BUCKET_NAME))
            # TODO: generalize to multiple bucket names
            | beam.ParDo(ReadImagesDoFn(bucket_name=IMAGES_BUCKET_NAME))
            | beam.ParDo(ImageToTfExampleDoFn())
            | beam.Map(lambda x: x.SerializeToString())
            | beam.io.tfrecordio.WriteToTFRecord(file_path_prefix=f'gs://{os.environ["TFRECORD_BUCKET"]}/images',
                                                 shard_name_template='-SSSSS-of-NNNNN.tfrecord')
    )
