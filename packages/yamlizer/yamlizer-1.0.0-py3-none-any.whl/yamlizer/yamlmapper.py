""" """

import inspect
from typing import Any


class YamlMappingError(Exception):
    """ """


def yaml_map(yamlizable: Any) -> dict[str, Any]:
    """[summary]

    Args:
        yamlizable (Any): [description]

    Raises:
        YamlMappingError: [description]

    Returns:
        dict[str, Any]: [description]
    """
    mro = inspect.getmro(type(yamlizable))
    yaml_map_keys = set()
    for class_ in mro:
        found_kwargs = False  # if true, visit parent class' __init__()
        init_params = inspect.signature(class_.__init__).parameters.values()

        for param in init_params:
            is_param_unbound = param.kind in (param.VAR_KEYWORD, param.VAR_POSITIONAL)
            is_yaml_map_key = not param.name == "self" and not is_param_unbound
            if is_yaml_map_key:
                yaml_map_keys.add(param.name)
            if param.kind == param.VAR_KEYWORD:
                found_kwargs = True
        if not found_kwargs:
            break

    yaml_map = dict()
    for key in yaml_map_keys:
        if not hasattr(yamlizable, key):
            raise YamlMappingError(f"'{key}' must be an attribute of '{yamlizable}'")
        else:
            value = getattr(yamlizable, key)
            yaml_map[key] = value
    return yaml_map
