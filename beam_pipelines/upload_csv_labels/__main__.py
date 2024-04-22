import argparse
import os

import apache_beam as beam
from apache_beam.io.jdbc import ReadFromJdbc
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.typehints.schemas import MillisInstant, LogicalType

LogicalType.register_logical_type(MillisInstant)


parser = argparse.ArgumentParser()
parser.add_argument(
    '--project',
    required=True,
    help='Project to read labels from.')

known_args, pipeline_args = parser.parse_known_args()

pipeline_options = PipelineOptions(pipeline_args)

with beam.Pipeline(options=pipeline_options) as p:
    pipeline = (
            p
            | ReadFromJdbc(
                query=f"SELECT label, gcs_url FROM labels_for_processing "
                      f"WHERE project='{known_args.project}';",
                table_name="users",
                driver_class_name="org.postgresql.Driver",
                jdbc_url=f"jdbc:postgresql://{os.environ.get('INSTANCE_NAME')}/{os.environ.get('POSTGRES_DB')}",
                username=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD")
            )
            | beam.Map(lambda elem: f"{elem[0]},{elem[1]}")
    )

    pipeline | beam.io.WriteToText("my_labels.csv", shard_name_template="")
    pipeline | "Show csv" >> beam.Map(print)
    pipeline | beam.combiners.Count.Globally() | "Count" >> beam.Map(print)
