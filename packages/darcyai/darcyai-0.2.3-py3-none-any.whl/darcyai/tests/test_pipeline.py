import numpy as np
import pytest
from unittest.mock import Mock, patch, MagicMock
from ..pipeline import Pipeline
from ..input.input_stream import InputStream
from ..output.output_stream import OutputStream


class TestPipeline:
    def test_constructor(self):
        pipeline = Pipeline(InputStream())
        assert pipeline is not None


    def test_constructor_validates_input_stream_not_none(self):
        with pytest.raises(Exception) as context:
            pipeline = Pipeline(None)
            
        assert "input_stream is required" in str(context.value)


    def test_constructor_validates_input_stream_type(self):
        with pytest.raises(Exception) as context:
            pipeline = Pipeline(1)
            
        assert "input_stream must be an instance of InputStream" in str(context.value)


    def test_add_output_stream_validates_not_none(self):
        pipeline = Pipeline(InputStream())

        with pytest.raises(Exception) as context:
            pipeline.add_output_stream(None)            

        assert "output_stream is required" in str(context.value)


    def test_add_output_stream_validates_type(self):
        pipeline = Pipeline(InputStream())

        with pytest.raises(Exception) as context:
            pipeline.add_output_stream(1)
            
        assert "output_stream must be an instance of OutputStream" in str(context.value)
