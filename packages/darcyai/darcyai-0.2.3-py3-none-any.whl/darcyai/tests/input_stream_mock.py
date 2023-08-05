import time
from ..input.input_stream import InputStream
from ..stream_data import StreamData


class InputStreamMock(InputStream):
    def __init__(self, iter, mock):
        self.__stopped = True
        self.__iter = iter
        self.__mock = mock


    def stop(self):
        self.__stopped = True
        self.__mock.stop()


    def stream(self):
        self.__stopped = False

        for i in self.__iter:
            self.__mock.stream(i)
            yield(StreamData(i, int(time.time() * 1000)))
            time.sleep(.1)
