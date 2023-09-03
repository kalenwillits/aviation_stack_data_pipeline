import pytest

from main.py import AviationStackDataLoader


@pytest.mark.extract
class TestExtract:
    def test_flatten_data():
        module = AviationStackDataLoader()
        assert {"0_0": 0, "0_1": 1, "1_0": 0, "1_1": 1} == module.flatten_data({0: {0: 0, 1: 1}, 1: {0: 0, 1: 1}})
