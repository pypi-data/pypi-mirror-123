import threading
from typing import Any

from .perceptor.perceptor_node import PerceptorNode
from .perception_object_model import PerceptionObjectModel
from .stream_data import StreamData


class ProcessingEngine():
    """
    The ProcessingEngine class is responsible for running perceptors on Edge TPUs
    """


    def __init__(self, number_of_edge_tpus:int):
        """
        Initializes the ProcessingEngine
        :param number_of_edge_tpus: The number of Edge TPUs to use
        """
        self.__edge_tpu_locks = [threading.Lock() for _ in range(number_of_edge_tpus)]


    def run(self, perceptor_node:PerceptorNode, input_data:StreamData, pom:PerceptionObjectModel) -> [Any, [Any]]:
        """
        Runs the perceptor on the input data
        :param perceptor_node: The perceptor node to run
        :param input_data: The input data to run the perceptor on
        :param pom: The Perceptor Object Model
        :return: The output of the perceptor
        """
        self.__edge_tpu_locks[perceptor_node.accelerator_idx].acquire()
        print("running %s" % perceptor_node)

        try:
            if perceptor_node.multi:
               return [perceptor_node.run(data, pom) for data in input_data]
            else:
                return perceptor_node.run(input_data, pom)
        finally:
            self.__edge_tpu_locks[perceptor_node.accelerator_idx].release()
