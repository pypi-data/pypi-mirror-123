from typing import Any

from ..stream_data import StreamData
from darcyai.utils import validate_not_none


class Perceptor():
    """
    The Perceptor class is the base class for all perceptors.
    """


    def __init__(self, model_path:str):
        """
        Constructor for the Perceptor class.
        :param model_path: The path to the model file.
        """
        validate_not_none(model_path, "model_path is required")

        self.model_path = model_path


    def run(self, input_data:StreamData) -> Any:
        """
        Runs the perceptor on the input data.
        :param input_data: The input data to run the perceptor on.
        :return: The output data from the perceptor.
        """
        raise NotImplementedError("Perceptor.run() is not implemented")


    def load(self, accelerator_idx:[int, None]=None) -> None:
        """
        Loads the perceptor.
        :param accelerator_idx: The index of the Edge TPU accelerator to load the perceptor on.
        :return: None
        """
        raise NotImplementedError("Perceptor.load() is not implemented")