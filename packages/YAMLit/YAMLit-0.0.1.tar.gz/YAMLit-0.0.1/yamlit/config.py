from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import yaml
from yaml import Loader, Node

from yamlit.dumper import YamlItDumper
from yamlit.loader import YamlItLoader
from yamlit.register import YamlItRegister
from yamlit.structures import YamlItDependency, YamlItMapping


class YamlItConfig:
    def __init__(self, path: Path) -> None:
        self._config: Optional[YamlItMapping] = None
        self._path = path

        with self._path.open() as stream:
            self._loader = YamlItLoader(stream)

        self._loader.add_local_constructor(tag='!deps', constructor=self._dependency_constructor)

    def load(self) -> YamlItMapping:
        if self._config is not None:
            return self._config

        try:
            config = self._loader.get_single_data()
            if not isinstance(config, YamlItMapping):
                raise RuntimeError(f"Config {self._path} is not a dict")
            self._config = config
            return self._config
        finally:
            self._loader.dispose()

    def dump(self, path: Path) -> None:
        with path.open('w') as file:
            yaml.dump(self._config, file, Dumper=YamlItDumper)

    def register(self, *registers: YamlItRegister) -> None:
        for register in registers:
            for obj in register:
                self._loader.add_local_constructor(tag=obj.tag, constructor=obj.construct)

    def _dependency_constructor(self, loader: Loader, node: Node) -> Any:
        value = loader.construct_yaml_str(node)
        value, _, attribute = value.partition(':')
        is_callable = attribute.endswith('()')
        if is_callable:
            attribute = attribute[:-2]
        return YamlItDependency(
            config=self,
            reference=value,
            attribute=attribute,
            is_callable=is_callable,
        )
