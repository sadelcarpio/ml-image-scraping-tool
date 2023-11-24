import os
import unittest
from datetime import datetime
from io import BytesIO
from unittest.mock import Mock
from unittest.mock import patch, MagicMock

import apache_beam as beam
import tensorflow as tf
from PIL import Image
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to

from pipelines.to_tfrecord.__main__ import ToTFRecordPipeline
from pipelines.to_tfrecord.image_dofns import DecodeFromTextDoFn, ReadImagesDoFn, ImageToTfExampleDoFn


class TestDecodeFromTextDoFn(unittest.TestCase):

    def test_process(self):
        elements = ['gs://bucket/path/to/image1.jpg,0',
                    'gs://bucket/path/to/image2.jpg,1',
                    'gs://bucket/path/to/image3.jpg,2']
        expected_output = [["path/to/image1.jpg", "0"],
                           ["path/to/image2.jpg", "1"],
                           ["path/to/image3.jpg", "2"]]
        with TestPipeline() as p:
            input_p = p | beam.Create(elements)
            output_p = input_p | beam.ParDo(DecodeFromTextDoFn())
            assert_that(
                output_p,
                equal_to(expected_output)
            )


class TestReadImagesDoFn(unittest.TestCase):
    @patch('pipelines.to_tfrecord.image_dofns.Client')
    def test_process(self, mock_gcs_client):
        fake_blob = Mock()
        fake_blob.download_as_bytes.return_value = b"fake-bytes"
        mock_bucket = Mock()
        mock_bucket.blob.return_value = fake_blob
        mock_gcs_client.return_value.bucket.return_value = mock_bucket

        elements = [["path/to/image1.jpg", 0]]
        expected_output = [(b"fake-bytes", 0)]

        with TestPipeline() as p:
            input_p = p | beam.Create(elements)
            output_p = input_p | beam.ParDo(ReadImagesDoFn(bucket_name="fake-bucket"))
            assert_that(
                output_p,
                equal_to(expected_output)
            )


class TestImageToTfExampleDoFn(unittest.TestCase):

    def setUp(self):
        self.image_data = Image.new('RGB', (50, 50), color='red')
        img_byte_arr = BytesIO()
        self.image_data.save(img_byte_arr, format='JPEG')
        self.img_encoded = img_byte_arr.getvalue()

    def test_bytes_feature(self):
        img_feature = ImageToTfExampleDoFn._bytes_feature(self.img_encoded)
        self.assertTrue(isinstance(img_feature, tf.train.Feature))

    def test_int64_feature(self):
        int_feature = ImageToTfExampleDoFn._int64_feature(123)
        self.assertTrue(isinstance(int_feature, tf.train.Feature))

    def test_process(self):
        label = 1
        input_data = [(self.img_encoded, label)]
        expected_output = [
            tf.train.Example(
                features=tf.train.Features(
                    feature={
                        'height':
                            tf.train.Feature(int64_list=tf.train.Int64List(value=[self.image_data.size[1]])),
                        'width':
                            tf.train.Feature(int64_list=tf.train.Int64List(value=[self.image_data.size[0]])),
                        'image_raw':
                            tf.train.Feature(bytes_list=tf.train.BytesList(value=[self.img_encoded])),
                        'label':
                            tf.train.Feature(int64_list=tf.train.Int64List(value=[label])),
                    }))
        ]

        with TestPipeline() as p:
            input_p = p | beam.Create(input_data)
            output_p = input_p | beam.ParDo(ImageToTfExampleDoFn())
            assert_that(
                output_p, equal_to(expected_output)
            )
