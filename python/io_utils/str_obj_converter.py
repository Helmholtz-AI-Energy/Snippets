from typing import TypeVar, Union

OBJ = TypeVar('OBJ')


def find_in(module, obj: Union[str, OBJ]) -> OBJ:
    """
    Used to input either a function/class or its name and return it from the given module

    e.g. for activation functions:
    getattr(nn, activation)() if isinstance(activation, str) else activation -> find_in(torch.nn, activation)
    """
    return getattr(module, obj) if isinstance(obj, str) else obj