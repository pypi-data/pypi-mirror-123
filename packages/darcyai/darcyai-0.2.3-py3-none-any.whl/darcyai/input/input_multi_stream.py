import threading
from typing import Callable, Iterable

from darcyai.input.input_stream import InputStream
from darcyai.stream_data import StreamData
from darcyai.utils import validate_not_none, validate_type


class InputMultiStream:
    """
    A class that represents a collection of input streams.
    """


    def __init__(self, aggregator:Callable[[None], StreamData], callback:Callable[[StreamData], None]):
        """
        Constructor for InputMultiStream.
        :param aggregator: a function that takes a list of data and returns a single data point
        :param callback: a function that gets called when data is received from a stream
        """
        validate_not_none(aggregator, "aggregator is required")
        validate_not_none(callback, "callback is required")

        self.__callback = callback
        self.__aggregator = aggregator

        self.__input_streams = {}
        self.__input_stream_threads = {}
        self.__stopped = True


    def remove_stream(self, name:str) -> None:
        """
        Removes a stream from the collection.
        :param name: the name of the stream to remove
        :return: None
        """
        if not name in self.__input_streams:
            return

        self.__input_streams[name].stop()
        if name in self.__input_stream_threads:
            self.__input_stream_threads.pop(name)

        self.__input_streams.pop(name)


    def get_stream(self, name:str) -> InputStream:
        """
        Gets a stream from the collection.
        :param name: the name of the stream to get
        :return: the stream
        """
        if not name in self.__input_streams:
            return None

        return self.__input_streams[name]


    def add_stream(self, name:str, stream:InputStream) -> None:
        """
        Adds a stream to the collection.
        :param name: the name of the stream to add
        :param stream: the stream to add
        :return: None
        """
        validate_not_none(stream, "stream is required")
        validate_type(stream, (InputStream, InputMultiStream), "stream is not of type InputStream")
        if name in self.__input_streams:
            raise Exception("stream with name %s already exists" % name)

        self.__input_streams[name] = stream

        if not self.__stopped:
            self.__input_stream_threads[name] = threading.Thread(target=self.__start_stream, args=[name])
            self.__input_stream_threads[name].start()


    def stream(self) -> Iterable[StreamData]:
        """
        Starts streaming data from all streams in the collection.
        :return: an iterator that yields data from all streams
        """
        if len(self.__input_streams) == 0:
            raise Exception("at least 1 stream is required")

        self.__stopped = False

        for stream_name in self.__input_streams.keys():
            self.__input_stream_threads[stream_name] = threading.Thread(target=self.__start_stream, args=[stream_name])
            self.__input_stream_threads[stream_name].start()

        while not self.__stopped:
            data = self.__aggregator()

            yield(data)


    def stop(self) -> None:
        """
        Stops streaming data from all streams in the collection.
        :return: None
        """
        for stream in self.__input_streams.values():
            stream.stop()

        self.__stopped = True

    
    def __start_stream(self, stream_name:str) -> None:
        """
        Starts the stream.
        :param stream_name: the name of the stream to start
        :return: None
        """
        input_stream = self.__input_streams[stream_name]
        stream = input_stream.stream()
        validate_type(stream, Iterable, "stream %s is not of type Iterable" % stream_name)

        for data in stream:
            self.__callback(stream_name, data)
