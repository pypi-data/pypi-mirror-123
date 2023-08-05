import time
from pycoral.utils import edgetpu
from random import random
from typing import Any

from darcyai.perceptor.perceptor import Perceptor
from darcyai.stream_data import StreamData
from darcyai.utils import validate_not_none, validate_type, validate


class ObjectDetectionPerceptor(Perceptor):
    """
    ObjectDetectionPerceptor is a class that implements the Perceptor interface for object detection.
    """


    def __init__(self, threshold:float, **kwargs):
        """
        Constructor for ObjectDetectionPerceptor.
        :param threshold: float, the threshold for object detection.
        """
        super().__init__(**kwargs)

        validate_not_none(threshold, "threshold is required")
        validate_type(threshold, (float, int), "threshold must be a number")
        validate(threshold >= 0 and threshold <= 1, "threshold must be between 0 and 1")

        self.__threshold = threshold
        self.__interpreter = None


    def run(self, input_data:StreamData) -> Any:
        """
        Runs the object detection model on the input data.
        :param input_data: StreamData, the input data to run the model on.
        :return: the output data from the model.
        """
        time.sleep(int(random() * 4) + 1)

        return "Hello!!!"


    def load(self, accelerator_idx:[int, None]) -> None:
        """
        Loads the object detection model.
        :param accelerator_idx: int, the index of the Edge TPU to use.
        :return: None
        """
        if accelerator_idx is None:
            self.__interpreter = edgetpu.make_interpreter(perceptor.model_path)
        else:
            self.__interpreter = edgetpu.make_interpreter(perceptor.model_path, device=':%s' % accelerator_idx)

        self.__interpreter.allocate_tensors()
