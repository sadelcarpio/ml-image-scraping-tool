# URL App
Microservice for reading URLs published to Kafka and upload to DB and distribute them across multiple users via a consistent hashing algorithm.

## Run locally (requires a postgres connection)
```shell
$ python3 -m src.main
```
Previously having set up environment variables: `DB_USER`, `DB_NAME`, `DB_PASSWORD`, `INSTANCE_NAME`, `MSG_TOPIC`. For listening to a local kafka broker, additionally `KAFKA_LISTENER`
