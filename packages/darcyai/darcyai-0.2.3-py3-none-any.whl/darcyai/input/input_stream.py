from typing import Iterable

from darcyai.stream_data import StreamData


class InputStream:
    """
    A class for reading input from a stream.
    """


    def __init__(self):
        pass

    def stream(self) -> Iterable[StreamData]:
        """
        Returns a generator that yields a stream of input.
        :return: A generator that yields a stream of input.
        """
        raise NotimplementedError("InputStream.stream() not implemented")


    def stop(self) -> None:
        """
        Stops the stream.
        :return: None
        """
        raise NotimplementedError("InputStream.stop() not implemented")
