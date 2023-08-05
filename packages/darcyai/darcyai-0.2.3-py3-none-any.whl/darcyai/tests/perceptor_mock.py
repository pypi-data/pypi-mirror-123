import time
from random import random
from darcyai.perceptor.perceptor import Perceptor


class PerceptorMock(Perceptor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def run(self, input_data):
        time.sleep(int(random() * 4) + 1)

        return "Hello!!!"
