import confluent_kafka


class KafkaConsumer(confluent_kafka.Consumer):
    def __init__(self, bootstrap_servers: str, group_id: str, topic: str) -> None:
        super().__init__({'bootstrap.servers': bootstrap_servers, 'group.id': group_id})
        self.topic = topic
        self.subscribe([self.topic])

    def read_urls(self):
        try:
            while True:
                msg = self.poll(1.0)
                if msg is None:
                    print("Waiting ...")
                elif msg.error():
                    print(f"ERROR: {msg.error()}")
                else:
                    print(f"Consumed event from topic {self.topic}: value = "
                          f"{msg.value().decode('utf-8')}")
        except:
            print("Something went wrong")
        finally:
            self.close()
