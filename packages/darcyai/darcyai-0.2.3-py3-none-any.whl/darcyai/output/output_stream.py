from typing import Iterable

from darcyai.stream_data import StreamData


class OutputStream:
    """
    OutputStream is a class that is used to write output to a stream.
    """
    def __init__(self):
        pass

    def stream(self) -> Iterable[StreamData]:
        """
        Returns the stream that this output stream is writing to.
        :return: The stream that this output stream is writing to.
        """
        raise NotImplementedError("OutputStream.stream() not implemented")


    def stop(self) -> None:
        """
        Stops the output stream.
        :return: None
        """
        raise NotImplementedError("OutputStream.stop() not implemented")
