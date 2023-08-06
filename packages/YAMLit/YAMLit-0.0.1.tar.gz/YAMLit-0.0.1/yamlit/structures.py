from __future__ import annotations

import typing
from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

if typing.TYPE_CHECKING:
    from yamlit.config import YamlItConfig


class YamlItType(metaclass=ABCMeta):
    @abstractmethod
    def eval(self) -> Any:
        raise NotImplementedError


class YamlItMapping(YamlItType, dict):
    def __init__(self, **kwargs) -> None:
        super(YamlItMapping, self).__init__(**kwargs)

    def eval(self) -> Dict[str, Any]:
        return {k: v.eval() if isinstance(v, YamlItType) else v for k, v in self.items()}

    def __getitem__(self, key: str) -> Any:
        key, _, sub_key = str(key).strip('.').partition('.')

        if not key:
            raise KeyError("Key cannot be empty")

        obj = super().__getitem__(key)

        if sub_key:
            return obj[sub_key]

        if isinstance(obj, YamlItScalar):
            return obj.eval()

        return obj

    def __setitem__(self, key: str, value: Any) -> None:
        if '.' in key:
            raise KeyError("Key cannot contain a period")

        super().__setitem__(key, value)


class YamlItSequence(YamlItType, list):
    def __init__(self, *args) -> None:
        super(YamlItSequence, self).__init__(*args)

    def eval(self) -> List[Any]:
        return [v.eval() if isinstance(v, YamlItType) else v for v in self]

    def __getitem__(self, item: Union[int, str]) -> Any:  # type: ignore
        key, _, sub_key = str(item).strip('.').partition('.')

        if not key:
            raise KeyError("Key cannot be empty")

        obj = super(YamlItSequence, self).__getitem__(int(key))

        if sub_key:
            return obj[sub_key]

        if isinstance(obj, YamlItScalar):
            return obj.eval()

        return obj


class YamlItScalar(YamlItType, metaclass=ABCMeta):
    pass


class YamlItLazyObject(YamlItScalar):
    def __init__(
        self,
        tag: str,
        obj: Callable,
        args: Tuple[Any, ...] = tuple(),
        kwargs: Optional[Dict[str, Any]] = None,
        call: bool = True,
    ) -> None:
        super(YamlItLazyObject, self).__init__()
        self._tag = tag
        self._obj = obj
        self._args = args
        self._kwargs = kwargs or dict()
        self._call = call

        self._return: Any = None
        self._evaluated: bool = False

    def eval(self) -> Any:
        if not self._evaluated:
            if self._call:
                self._return = self._obj(*self._args, **self._kwargs)
            else:
                self._return = self._obj
            self._evaluated = True
        return self._return

    def __str__(self) -> str:
        return str(self._obj)

    def __repr__(self) -> str:
        return repr(self._obj)

    @property
    def tag(self) -> str:
        return self._tag

    @property
    def obj(self) -> Callable:
        return self._obj

    @property
    def args(self) -> Tuple[Any, ...]:
        return self.args

    @property
    def kwargs(self) -> Dict[str, Any]:
        return self._kwargs

    @property
    def call(self) -> bool:
        return self._call


class YamlItDependency(YamlItScalar):
    def __init__(
        self,
        config: YamlItConfig,
        reference: str,
        attribute: str,
        is_callable: bool,
    ) -> None:
        super(YamlItDependency, self).__init__()
        self._config = config
        self._reference = reference
        self._attribute = attribute
        self._is_callable = is_callable

    @property
    def object(self) -> Any:
        return self._config.load()[self._reference]

    def eval(self) -> Any:
        if self._attribute:
            if self._is_callable:
                return getattr(self.object, self._attribute)()
            return getattr(self.object, self._attribute)
        return self.object

    def __str__(self) -> str:
        attr = f":{self._attribute}" if self._attribute else ""
        call = "()" if self._is_callable else ""
        return self._reference + attr + call

    def __repr__(self) -> str:
        return str(self)

    @property
    def reference(self) -> str:
        return self._reference

    @property
    def attribute(self) -> str:
        return self._attribute

    @property
    def is_callable(self) -> bool:
        return self._is_callable
