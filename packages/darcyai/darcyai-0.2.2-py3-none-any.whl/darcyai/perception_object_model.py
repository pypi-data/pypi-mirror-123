from typing import Any


class PerceptionObjectModel():
    """
    This class is used to represent the perception of an object.
    """


    def __init__(self):
        """
        Initialize the perception object model.
        """
        self.__dict__ = {}


    def set_value(self, key:str, value:Any) -> None:
        """
        Set the value of a key in the perception object model.
        :param key: The key to set.
        :param value: The value to set.
        :return: None
        """
        self.__dict__[key] = value