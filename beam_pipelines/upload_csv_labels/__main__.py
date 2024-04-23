import argparse
import os
from dataclasses import dataclass

import apache_beam as beam
from apache_beam.io.jdbc import ReadFromJdbc
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.typehints.schemas import MillisInstant, LogicalType

LogicalType.register_logical_type(MillisInstant)


@dataclass
class DbParams:
    instance_name: str
    postgres_db: str
    postgres_user: str
    postgres_password: str

    def jdbc_string(self) -> str:
        return f"jdbc:postgresql://{self.instance_name}/{self.postgres_db}"


class PsqlToCsvPipeline(beam.PTransform):
    def __init__(self, project: str, db_params: DbParams):
        super().__init__()
        self.project = project
        self.db_params = db_params

    def expand(self, p):

        pipeline = (
                p
                | ReadFromJdbc(
                    query=f"SELECT label, gcs_url FROM labels_for_processing "
                          f"WHERE project='{self.project}';",
                    table_name="users",
                    driver_class_name="org.postgresql.Driver",
                    jdbc_url=self.db_params.jdbc_string(),
                    username=self.db_params.postgres_user,
                    password=self.db_params.postgres_password
                )
                | beam.Map(lambda elem: f"{elem[0]},{elem[1]}")
        )

        pipeline | beam.io.WriteToText("my_labels.csv", shard_name_template="")
        pipeline | "Show csv" >> beam.Map(print)
        pipeline | beam.combiners.Count.Globally() | "Count" >> beam.Map(print)
        return pipeline


def run_pipeline():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--project',
        required=True,
        help='Project to read labels from.')

    known_args, pipeline_args = parser.parse_known_args()

    pipeline_options = PipelineOptions(pipeline_args)

    db_params = DbParams(instance_name=os.environ["INSTANCE_NAME"],
                         postgres_db=os.environ["POSTGRES_DB"],
                         postgres_user=os.environ["POSTGRES_USER"],
                         postgres_password=os.environ["POSTGRES_PASSWORD"])

    with beam.Pipeline(options=pipeline_options) as p:
        (
            p | PsqlToCsvPipeline(project=known_args.project,
                                  db_params=db_params)
        )


if __name__ == '__main__':
    run_pipeline()
