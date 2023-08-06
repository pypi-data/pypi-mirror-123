""" """

import inspect
from pathlib import Path
from typing import Any, Type

import yaml

from . import yamlmapper


class YamlRegistrationError(Exception):
    """ """


class YamlizationError(Exception):
    """ """


class _YamlRegistrar:
    """ """

    def __init__(self) -> None:
        self.register: dict[str, Type] = dict()


_REGISTRAR = _YamlRegistrar()


def register(cls: Type[Any]) -> None:
    """ """
    if not inspect.isclass(cls):
        raise YamlRegistrationError("Only Python class(es) can be registered")
    yaml_tag = cls.__name__
    yaml.SafeDumper.add_representer(cls, _represent)
    yaml.SafeLoader.add_constructor(yaml_tag, _construct)
    _REGISTRAR.register[yaml_tag] = cls


def _represent(dumper: yaml.Dumper, yamlizable: Any) -> yaml.MappingNode:
    """ """
    yaml_tag = yamlizable.__class__.__name__
    yaml_map = yamlmapper.yaml_map(yamlizable)
    return dumper.represent_mapping(yaml_tag, yaml_map)


def _construct(loader: yaml.Loader, node: yaml.MappingNode) -> Any:
    """ """
    kwargs = loader.construct_mapping(node, deep=True)
    cls = _REGISTRAR.register[node.tag]
    try:
        return cls(**kwargs)
    except TypeError:
        raise YamlizationError(f"Yaml map incompatible with {cls} init()") from None


def dump(config: Any, configpath: Path, mode: str = "w+") -> None:
    """ """
    with open(configpath, mode=mode) as configfile:
        yaml.safe_dump(config, configfile)


def load(configpath: Path) -> Any:
    """ """
    with open(configpath, mode="r") as configfile:
        return yaml.safe_load(configfile)
