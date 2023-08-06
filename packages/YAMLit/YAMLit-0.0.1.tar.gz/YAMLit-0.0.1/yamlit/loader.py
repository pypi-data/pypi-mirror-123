import os
import re
from pathlib import Path
from typing import BinaryIO, Callable, Iterable, TextIO, Union

from yaml import Node, SafeLoader

from yamlit.structures import YamlItMapping, YamlItSequence


class YamlItLoader(SafeLoader):
    ENV_SEPARATOR = ':'
    ENV_PATTERN = re.compile(r'.*?\${(.*?)}.*?')

    def __init__(self, stream: Union[BinaryIO, TextIO]) -> None:
        super(YamlItLoader, self).__init__(stream)

        self.yaml_constructors = self.yaml_constructors.copy()
        self.yaml_multi_constructors = self.yaml_multi_constructors.copy()

    def add_local_constructor(self, tag: str, constructor: Callable) -> None:
        self.yaml_constructors[tag] = constructor

    def add_local_multi_constructor(self, tag: str, constructor: Callable) -> None:
        self.yaml_constructors[tag] = constructor

    def construct_yaml_seq(self, node: Node) -> Iterable[YamlItSequence]:
        data = YamlItSequence()
        yield data
        data.extend(self.construct_sequence(node))

    def construct_yaml_map(self, node: Node) -> Iterable[YamlItMapping]:
        data = YamlItMapping()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_env_var(self, node: Node) -> Path:
        value = self.construct_yaml_str(node)
        for group in self.ENV_PATTERN.findall(value):
            key, _, default = str(group).partition(self.ENV_SEPARATOR)
            value = value.replace(f"${{{group}}}", os.environ.get(key, default=default))
        return value

    def construct_path(self, node: Node) -> Path:
        value = self.construct_yaml_str(node)
        return Path(value)


YamlItLoader.add_constructor(tag='!env',
                             constructor=YamlItLoader.construct_env_var)
YamlItLoader.add_constructor(tag='!path',
                             constructor=YamlItLoader.construct_path)
YamlItLoader.add_constructor(tag='tag:yaml.org,2002:seq',
                             constructor=YamlItLoader.construct_yaml_seq)
YamlItLoader.add_constructor(tag='tag:yaml.org,2002:map',
                             constructor=YamlItLoader.construct_yaml_map)
