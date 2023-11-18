import io
import re

import apache_beam as beam
import numpy as np
import tensorflow as tf
from PIL import Image
from google.cloud.storage import Client


class DecodeFromTextDoFn(beam.DoFn):
    def __init__(self, bucket_name):
        super().__init__()
        self.bucket_name = bucket_name

    def process(self, element, *args, **kwargs):
        path, label = element.split(",")
        path = re.split(rf"gs://{self.bucket_name}/", path)[1]
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
        image_bytes = io.BytesIO(blob.download_as_bytes())
        img = np.array(Image.open(image_bytes))
        yield img, label

    def teardown(self):
        self.gcs_client.close()


class ImageToTfExampleDoFn(beam.DoFn):

    @staticmethod
    def _bytes_feature(value):
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

    def process(self, element, *args, **kwargs):
        img, label = element
        img = img.astype(np.float32)
        label = np.array(label, dtype=np.float32)
        example = tf.train.Example(
            features=tf.train.Features(
                feature={'image': self._bytes_feature(img.tostring()),
                         'label': self._bytes_feature(label.tostring())}
            )
        )
        yield example
