import os

import apache_beam as beam

from to_tfrecord.image_dofns import DecodeFromTextDoFn, ReadImagesDoFn, ImageToTfExampleDoFn

CATS_BUCKET_NAME = os.environ["CATS_BUCKET_NAME"]

with beam.Pipeline() as p:

    pipeline = (
            p
            | beam.io.ReadFromText("beam_pipelines/data_labeled.csv", skip_header_lines=1)
            | beam.ParDo(DecodeFromTextDoFn(bucket_name=CATS_BUCKET_NAME))
            | beam.ParDo(ReadImagesDoFn(bucket_name=CATS_BUCKET_NAME))
            | beam.ParDo(ImageToTfExampleDoFn())
            | beam.Map(lambda x: x.SerializeToString())
            | beam.io.tfrecordio.WriteToTFRecord(file_path_prefix='beam_pipelines/labeled',
                                                 shard_name_template='-SSSSS-of-NNNNN.tfrecord')
    )
