# Kafka Web Page Producer

Downloads HTML code from a HTTP source and sends them to a kafka topic.

## Usage

### Environment

- BOOTSTRAP_SERVERS list of Kafka bootstrap servers to connect to
- RETRIEVE_INTERVAL html retrieval interval (default:60)

### Configure the source

```json
{
  "url": "https://example.com",
  "topic": "some-topic"
}
```

- **topic** Kafka topic to post into
- **url** web page url


### Run the container

To run the container locally use `--network-host`

```shell
docker run --network=host -e BOOTSTRAP_SERVERS="localhost:9092" --rm kafkawebpageproducer:local
```
