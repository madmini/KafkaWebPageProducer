import logging
import time
from datetime import datetime
from json import dumps
from os import environ
from urllib.error import URLError
from urllib.request import urlretrieve

from kafka import KafkaProducer

from util.page_config import PageConfig

env_name_bootstrap_server = "BOOTSTRAP_SERVERS"
env_name_interval = "RETRIEVE_INTERVAL"

default_retrieve_interval = 60

def get_page(url):
    """
    Retrieve a webpage from a URL and return its contents
    :param url: URL
    :return:
    """
    tmp_file, _ = urlretrieve(url)
    with open(tmp_file) as f:
        return f.read()


def get_retrieve_interval() -> int:
    interval = environ.get(env_name_interval)
    retrieve_interval = default_retrieve_interval
    if not interval:
        logging.info(f"{env_name_interval} not set, using {default_retrieve_interval} seconds")
    else:
        retrieve_interval = int(interval)
        logging.info(f"{env_name_interval} set, using {retrieve_interval} seconds")
    return retrieve_interval


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    boostrap_server = environ.get(env_name_bootstrap_server)
    if not boostrap_server:
        raise EnvironmentError(f"Set {env_name_bootstrap_server} in environment")

    retrieve_interval = get_retrieve_interval()
    p = PageConfig.from_file("page_config.json")
    logging.info(f"Getting pages from {p.url} ...")
    producer = KafkaProducer(bootstrap_servers=boostrap_server)
    # value_serializer=lambda rec: dumps(rec.to_json()).encode('utf-8')
    while True:
        try:
            page_data = get_page(p.url)
            r = producer.send(p.topic, page_data.encode("utf-8"))
            with open(f"pages/{datetime.now().timestamp()}.html", 'w') as f:
                f.write(page_data)
            while not r.is_done:
                time.sleep(0.1)
            logging.info(f"Wrote page with offset {r.value.offset} and timestamp {r.value.timestamp}")
        except URLError:
            logging.warning(f"Could not fetch page from URL {p.url} .. retrying in {retrieve_interval} seconds")
        time.sleep(retrieve_interval)
