import apache_beam as beam
from apache_beam.io.jdbc import ReadFromJdbc

with beam.Pipeline() as p:
    pipeline = (
            p
            | ReadFromJdbc(
                query="SELECT username FROM users;",
                table_name="users",
                driver_class_name="org.postgresql.Driver",
                jdbc_url="jdbc:postgresql://test-postgres:5432/test",
                username="test",
                password="test"
            ) | beam.Map(print)
    )
