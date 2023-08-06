from __future__ import annotations

from typing import Callable, Optional

from yaml import Loader, MappingNode, Node, ScalarNode, SequenceNode

from yamlit.structures import YamlItLazyObject, YamlItType


class YamlItRegister(list):
    def __init__(self, name: Optional[str] = None) -> None:
        super(YamlItRegister, self).__init__()
        self._name = name

    @property
    def name(self) -> Optional[str]:
        return self._name

    def register(self, name: str, obj: Callable) -> YamlItRegister:
        if self._name:
            name = f'{self._name}.{name}'
        self.append(YamlItLazyObjectRegister(name=name, obj=obj))
        return self


class YamlItLazyObjectRegister:
    POSITIONAL_ARGUMENT_KEY = '__pos__'

    def __init__(self, name: str, obj: Callable) -> None:
        self._tag = f"!@{name}"
        self._obj = obj

    @property
    def tag(self):
        return self._tag

    def construct(self, loader: Loader, node: Node) -> YamlItType:
        if isinstance(node, ScalarNode):
            return YamlItLazyObject(
                tag=self._tag,
                obj=self._obj,
                call=False,
            )
        elif isinstance(node, SequenceNode):
            args = loader.construct_sequence(node)
            return YamlItLazyObject(
                tag=self._tag,
                obj=self._obj,
                args=args,
                call=True,
            )
        elif isinstance(node, MappingNode):
            kwargs = loader.construct_mapping(node)
            return YamlItLazyObject(
                tag=self._tag,
                obj=self._obj,
                args=kwargs.pop(self.POSITIONAL_ARGUMENT_KEY, tuple()),
                kwargs=kwargs,
                call=True,
            )
        else:
            raise ValueError(f"Node {node} is not supported")
