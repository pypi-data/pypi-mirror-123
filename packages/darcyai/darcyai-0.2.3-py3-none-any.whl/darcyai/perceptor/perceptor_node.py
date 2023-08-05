from tflite_runtime.interpreter import Interpreter
from typing import Callable, Any

from darcyai.perceptor.perceptor import Perceptor
from darcyai.perception_object_model import PerceptionObjectModel
from darcyai.stream_data import StreamData
from darcyai.utils import validate_not_none, validate_type


class PerceptorNode:
    """
    PerceptorNode is a wrapper for the Perceptor object.
    """


    def __init__(self,
                 perceptor_name:str,
                 perceptor:Perceptor,
                 input_callback:Callable[[StreamData, PerceptionObjectModel], Any],
                 output_callback:Callable[[Any, PerceptionObjectModel], Any]=None,
                 multi:bool=False,
                 accelerator_idx:[int, None]=None):
        """
        :param perceptor_name: The name of the perceptor
        :param perceptor: The perceptor to run
        :param input_callback: The callback to run on the input data
        :param output_callback: The callback to run on the output data
        :param multi: Whether or not to run the perceptor for each item in input data
        :param accelerator_idx: The index of the Edge TPU to use
        """

        validate_not_none(perceptor, "perceptor is required")
        validate_type(perceptor, Perceptor, "perceptor must be an instance of Perceptor")

        validate_not_none(perceptor_name, "perceptor_name is required")
        validate_type(perceptor_name, str, "perceptor_name must be a string")

        validate_not_none(input_callback, "input_callback is required")
        validate_type(input_callback, Callable, "input_callback must be a function")

        if output_callback is not None:
            validate_type(output_callback, Callable, "output_callback must be a function")

        self.accelerator_idx = accelerator_idx
        self.multi = multi

        self.__name = perceptor_name
        self.__perceptor = perceptor
        self.__child_perceptors = []
        self.__input_callback = input_callback
        self.__output_callback = output_callback

        # self.__perceptor.load(accelerator_idx)


    def add_child_perceptor(self, perceptor_node) -> None:
        """
        Adds a child perceptor to this perceptor node
        :param perceptor_node: The perceptor node to add
        :return: None
        """
        validate_not_none(perceptor_node, "perceptor_node is required")
        validate_type(perceptor_node, str, "perceptor_node must be a string")

        self.__child_perceptors.append(perceptor_node)


    def get_child_perceptors(self) -> list:
        """
        Returns the child perceptors of this perceptor node
        :return: The child perceptors of this perceptor node
        """
        return self.__child_perceptors


    def run(self, input_data:StreamData, pom:PerceptionObjectModel) -> Any:
        """
        Runs the perceptor node
        :param input_data: The input data to run the perceptor on
        :param pom: The perception object model to use
        :return: The output of the perceptor
        """
        processed_input_data = self.__input_callback(input_data, pom)

        result = self.__perceptor.run(input_data)

        if self.__output_callback is not None:
            result = self.__output_callback(result, pom)

        print("finished running %s" % self.__str__())

        return result


    def __str__(self) -> str:
        """
        Returns the string representation of this perceptor node
        :return: The string representation of this perceptor node
        """
        return "PerceptorNode { name: %s }" % self.__name
