""" """

import yaml

from . import yamlmapper
from .yamlizer import YamlizationError


class YamlizableMetaclass(type):
    """ """

    def __init__(cls, name, bases, kwds) -> None:
        """ """
        super().__init__(name, bases, kwds)
        cls._yaml_tag = name
        cls._yaml_dumper = yaml.SafeDumper
        cls._yaml_dumper.add_representer(cls, cls._to_yaml)
        cls._yaml_loader = yaml.SafeLoader
        cls._yaml_loader.add_constructor(cls._yaml_tag, cls._from_yaml)

    def __repr__(cls) -> str:
        """ """
        return f"<class '{cls.__name__}>"


class Yamlizable(metaclass=YamlizableMetaclass):
    """ """

    def __repr__(self) -> str:
        """ """
        yaml_map = yamlmapper.yaml_map(self)
        yaml_map_items = [f"{k}={v!r}" for k, v in sorted(yaml_map.items())]
        return f"{self.__class__.__name__}({', '.join(yaml_map_items)})"

    @classmethod
    def _to_yaml(cls, dumper: yaml.Dumper, yamlizable) -> yaml.MappingNode:
        """ """
        yaml_map = yamlmapper.yaml_map(yamlizable)
        return dumper.represent_mapping(yamlizable._yaml_tag, yaml_map)

    @classmethod
    def _from_yaml(cls, loader: yaml.Loader, node: yaml.MappingNode):
        """ """
        try:
            kwargs = loader.construct_mapping(node, deep=True)
            return cls(**kwargs)
        except TypeError:
            raise YamlizationError(f"Yaml map incompatible with {cls} init()") from None
