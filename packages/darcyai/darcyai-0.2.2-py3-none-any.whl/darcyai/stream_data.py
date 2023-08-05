from typing import Any


class StreamData():
    """
    Class to hold data from a stream.
    """


    def __init__(self, data:Any, timestamp:int):
        """
        Initialize the StreamData object.
        :param data: The data to be stored.
        :param timestamp: The timestamp of the data.
        """
        self.data = data
        self.timestamp = timestamp
