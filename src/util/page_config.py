from dataclasses import dataclass
from json import loads


@dataclass
class PageConfig:
    url: str
    topic: str

    @staticmethod
    def from_file(file):
        with open(file) as f:
            dct = loads(f.read())
            return PageConfig(dct["url"], dct["topic"])
