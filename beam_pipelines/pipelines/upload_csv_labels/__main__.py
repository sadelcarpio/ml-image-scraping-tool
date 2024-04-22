import apache_beam as beam
from apache_beam.io.jdbc import ReadFromJdbc
from apache_beam.typehints.schemas import MillisInstant, LogicalType

LogicalType.register_logical_type(MillisInstant)

PROJECT = "test-project-full"  # pass as cmd argument

with beam.Pipeline() as p:
    pipeline = (
            p
            | ReadFromJdbc(
                query=f"SELECT label, gcs_url FROM labels_for_processing WHERE project='{PROJECT}';",
                table_name="users",
                driver_class_name="org.postgresql.Driver",
                jdbc_url="jdbc:postgresql://test-postgres:5432/test",
                username="test",
                password="test"
            )
            | beam.Map(lambda elem: f"{elem[0]},{elem[1]}")
    )

    pipeline | beam.io.WriteToText("my_labels.csv", shard_name_template="")
    pipeline | beam.Map(print)
