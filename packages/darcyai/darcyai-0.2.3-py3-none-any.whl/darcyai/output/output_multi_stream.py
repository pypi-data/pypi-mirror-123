import threading
from typing import Iterable, Callable

from darcyai.output.output_stream import OutputStream
from darcyai.stream_data import StreamData
from darcyai.utils import validate_not_none, validate_type


class OutputMultiStream:
    """
    A class that represents a collection of output streams.
    """


    def __init__(self, aggregator:Callable[[None], StreamData], callback:Callable[[StreamData], None]):
        """
        Constructor for OuputMultiStream.
        :param aggregator: a function that takes a list of data and returns a single data point
        :param callback: a function that gets called when data is availabke for a stream
        """
        validate_not_none(aggregator, "aggregator is required")
        validate_not_none(callback, "callback is required")

        self.__callback = callback
        self.__aggregator = aggregator

        self.__output_streams = {}
        self.__output_stream_threads = {}
        self.__stopped = True

    
    def __start_stream(self, stream_name:str) -> None:
        """
        Starts the stream.
        :param stream_name: the name of the stream
        :return: None
        """
        output_stream = self.__output_streams[stream_name]
        stream = output_stream.stream()
        validate_type(stream, Iterable, "stream %s is not of type Iterable" % stream_name)

        for data in stream:
            self.__callback(stream_name, data)


    def remove_stream(self, name:str) -> None:
        """
        Removes a stream from the collection.
        :param name: the name of the stream to remove
        :return: None
        """
        if not name in self.__output_streams:
            return

        self.__output_streams[name].stop()
        if name in self.__output_stream_threads:
            self.__output_stream_threads.pop(name)

        self.__output_streams.pop(name)


    def get_stream(self, name:str) -> OutputStream:
        """
        Gets a stream by name.
        :param name: the name of the stream
        :return: the stream
        """
        if not name in self.__output_streams:
            return None

        return self.__output_streams[name]


    def add_stream(self, name:str, stream:OutputStream) -> None:
        """
        Adds a stream to the collection.
        :param name: the name of the stream
        :param stream: the stream
        :return: None
        """
        validate_not_none(name, "name is required")
        validate_not_none(stream, "stream is required")
        validate_type(stream, (OutputStream, OutputMultiStream), "stream is not of type OutputStream")

        if name in self.__output_streams:
            raise Exception("stream with name %s already exists" % name)

        self.__output_streams[name] = stream

        if not self.__stopped:
            self.__output_stream_threads[name] = threading.Thread(target=self.__start_stream, args=[name])
            self.__output_stream_threads[name].start()


    def stream(self) -> Iterable[StreamData]:
        """
        Gets the stream.
        :return: the stream
        """
        if len(self.__output_streams) == 0:
            raise Exception("at least 1 stream is required")

        self.__stopped = False

        for stream_name in self.__output_streams.keys():
            self.__output_stream_threads[stream_name] = threading.Thread(target=self.__start_stream, args=[stream_name])
            self.__output_stream_threads[stream_name].start()

        while not self.__stopped:
            data = self.__aggregator()

            yield(data)


    def stop(self) -> None:
        """
        Stops the streams.
        :return: None
        """
        for stream in self.__output_streams.values():
            stream.stop()

        self.__stopped = True
