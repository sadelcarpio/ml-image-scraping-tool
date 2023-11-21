import io
import re

import apache_beam as beam
import tensorflow as tf
from PIL import Image
from google.cloud.storage import Client


class DecodeFromTextDoFn(beam.DoFn):

    def process(self, element, *args, **kwargs):
        path, label = element.split(",")
        path = re.split(rf"(gs://.+?/)", path)[2]
        return [[path, label]]


class ReadImagesDoFn(beam.DoFn):
    gcs_client = None
    bucket = None

    def __init__(self, bucket_name):
        super().__init__()
        self.bucket_name = bucket_name

    def setup(self):
        self.gcs_client = Client()
        self.bucket = self.gcs_client.bucket(self.bucket_name)

    def process(self, element, *args, **kwargs):
        path, label = element
        blob = self.bucket.blob(path)
        img_bytes = blob.download_as_bytes()
        yield img_bytes, label

    def teardown(self):
        self.gcs_client.close()


class ImageToTfExampleDoFn(beam.DoFn):

    @staticmethod
    def _bytes_feature(value):
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

    @staticmethod
    def _int64_feature(value):
        return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

    def process(self, element, *args, **kwargs):
        img_raw, label = element
        image_shape = Image.open(io.BytesIO(img_raw)).size
        example = tf.train.Example(
            features=tf.train.Features(
                feature={'height': self._int64_feature(image_shape[1]),
                         'width': self._int64_feature(image_shape[0]),
                         'image_raw': self._bytes_feature(img_raw),
                         'label': self._int64_feature(int(label))}
            )
        )
        yield example
