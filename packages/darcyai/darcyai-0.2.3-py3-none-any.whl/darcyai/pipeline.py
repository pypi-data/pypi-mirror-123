from collections.abc import Iterable
from multiprocessing.pool import ThreadPool
from pycoral.utils.edgetpu import list_edge_tpus
from typing import Callable, Any

from darcyai.cyclic_toposort import acyclic_toposort
from darcyai.input.input_multi_stream import InputMultiStream
from darcyai.input.input_stream import InputStream
from darcyai.output.output_stream import OutputStream
from darcyai.perceptor.perceptor import Perceptor
from darcyai.perceptor.perceptor_node import PerceptorNode
from darcyai.perception_object_model import PerceptionObjectModel
from darcyai.processing_engine import ProcessingEngine
from darcyai.stream_data import StreamData
from darcyai.utils import validate_not_none, validate_type, validate


class Pipeline():
    """
    The Pipeline class is the main class of the darcyai package.
    """


    def __init__(self, input_stream:InputStream):
        """
        Initializes a new instance of the Pipeline class.
        :param input_stream: The input stream to be used by the pipeline.
        """
        validate_not_none(input_stream, "input_stream is required")
        validate_type(input_stream, (InputStream, InputMultiStream), "input_stream must be an instance of InputStream")

        self.__input_stream = input_stream
        self.__num_of_edge_tpus = len(list_edge_tpus())
        self.__perceptors = {}
        self.__output_streams = []
        self.__processing_engine = ProcessingEngine(self.__num_of_edge_tpus)
        self.__thread_pool = ThreadPool(10)
        self.__pom = PerceptionObjectModel()

        self.__running = False


    def num_of_edge_tpus(self) -> int:
        """
        Gets the number of Edge TPUs in the pipeline.
        :return: The number of Edge TPUs in the pipeline.
        """
        return self.__num_of_edge_tpus


    def add_perceptor(self,
                      name: str,
                      perceptor: Perceptor,
                      input_callback:Callable[[StreamData, PerceptionObjectModel], Any],
                      output_callback:Callable[[Any, PerceptionObjectModel], Any]=None,
                      parent:str=None,
                      multi:bool=False,
                      accelerator_idx:[int, None]=None) -> None:
        """
        Adds a new Perceptor to the pipeline.
        :param name: The name of the Perceptor.
        :param perceptor: The Perceptor to be added.
        :param input_callback: The callback function to be called when the Perceptor receives a new input.
        :param output_callback: The callback function to be called when the Perceptor has finished processing.
        :param parent: The name of the parent Perceptor.
        :param multi: Whether or not to run the perceptor for each item in input data
        :param accelerator_idx: The index of the Edge TPU to be used by the Perceptor.
        :return: None
        """
        if self.__running:
            raise Exception("Pipeline is already running")

        validate_not_none(name, "name is required")
        validate_not_none(perceptor, "perceptor is required")
        validate_type(perceptor, Perceptor, "perceptor must be an instance of Perceptor")
        validate_not_none(input_callback, "input_callback is required")
        validate(callable(input_callback), "input_callback must be a function")

        if output_callback is not None:
            validate(callable(output_callback), "output_callback must be a function")

        if accelerator_idx is not None:
            validate_type(accelerator_idx, int, "accelerator_idx must be an integer")

            if accelerator_idx >= self.__num_of_edge_tpus:
                raise ValueError("accelerator_idx must be less than %d" % self.__num_of_edge_tpus)

        if parent is not None and self.__perceptors[parent] is None:
            raise ValueError("perceptor with name '%s' does not exist" % name)

        perceptor_node = PerceptorNode(name, perceptor, input_callback, output_callback, multi, accelerator_idx)

        self.__perceptors[name] = perceptor_node
        if parent is not None:
            self.__perceptors[parent].add_child_perceptor(name)


    def add_output_stream(self, output_stream:OutputStream) -> None:
        """
        Adds an OutputStream to the pipeline.
        :param output_stream: The OutputStream to be added.
        :return: None
        """
        validate_not_none(output_stream, "output_stream is required")
        validate_type(output_stream, OutputStream, "output_stream must be an instance of OutputStream")

        self.__output_streams.append(output_stream)


    def stop(self) -> None:
        """
        Stops the pipeline.
        :return: None
        """
        self.__running = False
        self.__input_stream.stop()


    def run(self) -> None:
        """
        Runs the pipeline.
        :return: None
        """
        self.__running = True

        try:
            stream = self.__input_stream.stream()
            validate_type(stream, Iterable, "input stream is not Iterable")

            perceptors_order = self.__get_perceptors_order()

            for input_data in stream:
                for perceptors in perceptors_order:
                    async_calls = [self.__thread_pool.apply_async(
                        self.__processing_engine.run,
                        args=(self.__perceptors[perceptor_name], input_data, self.__pom),
                        callback=self.__set_perceptor_result(perceptor_name)) for perceptor_name in perceptors]
                    [async_call.get() for async_call in async_calls]
        except Exception as e:
            print(e)
        finally:
            self.__running = False


    def __set_perceptor_result(self, perceptor_name:str) -> Callable[[Any], None]:
        """
        Sets the result of a Perceptor.
        :param perceptor_name: The name of the Perceptor.
        :return: The callback function to be called when the Perceptor has finished processing.
        """
        def set_result(result:Any) -> None:
            """
            Sets the result of a Perceptor in POM.
            :param result: The result of the Perceptor.
            :return: None
            """
            self.__pom.set_value(perceptor_name, result)

        return set_result


    def __get_perceptors_order(self) -> [str]:
        """
        Gets the order of the Perceptors in the pipeline.
        :return: The order of the Perceptors in the pipeline.
        """
        orphan_perceptors = []
        parent_perceptors = []
        visited = []

        for perceptor_name in self.__perceptors.keys():
            child_perceptors = self.__perceptors[perceptor_name].get_child_perceptors()
            if len(child_perceptors) == 0:
                if perceptor_name not in visited:
                    orphan_perceptors.append(perceptor_name)
            else:
                visited.append(perceptor_name)
                for child in child_perceptors:
                    parent_perceptors.append((perceptor_name, child))
                    visited.append(child)

        if len(parent_perceptors) > 0:
            perceptors_order = acyclic_toposort(parent_perceptors)
            [perceptors_order[0].add(x) for x in orphan_perceptors]
        else:
            perceptors_order = [{x for x in orphan_perceptors}]

        return perceptors_order
