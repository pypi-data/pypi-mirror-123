import inspect
from pathlib import Path
from typing import Any, Dict

from yaml import Node, SafeDumper

from yamlit.register import YamlItLazyObjectRegister
from yamlit.structures import YamlItDependency, YamlItLazyObject, YamlItMapping, YamlItSequence


class YamlItDumper(SafeDumper):
    POSITIONAL_ARGUMENT_KEY = YamlItLazyObjectRegister.POSITIONAL_ARGUMENT_KEY

    def represent_path(self, data: Path) -> Node:
        return self.represent_str(str(data))

    def represent_yamlit_callable(self, data: YamlItLazyObject) -> Node:
        representation: Dict[str, Any] = dict()
        parameters = inspect.signature(data.obj).parameters
        param_dict = {param.name: (param.kind, param.default) for param in parameters.values()}

        for name, (kind, default) in param_dict.items():
            default = default if default is not inspect.Parameter.empty else None
            if kind == inspect.Parameter.POSITIONAL_ONLY:
                if self.POSITIONAL_ARGUMENT_KEY not in representation:
                    representation[self.POSITIONAL_ARGUMENT_KEY] = list()
                representation[self.POSITIONAL_ARGUMENT_KEY].append(default)
            else:
                representation[name] = default

        node = self.represent_dict(representation)
        node.tag = data.tag
        return node

    def represent_yamlit_attribute(self, data: YamlItDependency) -> Node:
        node = self.represent_data(str(data))
        node.tag = '!deps'
        return node


YamlItDumper.add_representer(YamlItMapping, YamlItDumper.represent_dict)
YamlItDumper.add_representer(YamlItSequence, YamlItDumper.represent_list)
YamlItDumper.add_representer(YamlItLazyObject, YamlItDumper.represent_yamlit_callable)
YamlItDumper.add_representer(YamlItDependency, YamlItDumper.represent_yamlit_attribute)
YamlItDumper.add_multi_representer(Path, YamlItDumper.represent_path)
