import time
from typing import Any
from varname import nameof


def validate_not_none(property:Any, message:str) -> None:
    """
    Validates that the property is not None.
    :param property: the property to validate
    :param message: the message to raise if the property is None
    :return: None
    """
    validate(property is not None, message)


def validate_type(property:Any, clazz:Any, message:str) -> None:
    """
    Validates that the property is of the specified type.
    :param property: the property to validate
    :param clazz: the type to validate against
    :param message: the message to raise if the property is not of the specified type
    :return: None
    """
    validate(isinstance(property, clazz), message)


def validate(condition:bool, message:str) -> None:
    """
    Validates that the condition is true.
    :param condition: the condition to validate
    :param message: the message to raise if the condition is false
    :return: None
    """
    if condition is None or not condition:
        raise Exception(message)


def timestamp() -> int:
    """
    Returns the current timestamp in milliseconds.
    :return: the current timestamp in milliseconds
    """
    return int(time.time() * 1000)