import pytest

from aviationstack.client import AviationStackApiClient


@pytest.mark.module
@pytest.mark.api_client
@pytest.mark.live
class TestAviationStackClient:
    def test_payload_has_more_results_true(self):
        client = AviationStackApiClient(threshold=100)
        payload = {
            "pagination": {
                "count": 100,
                "offset": 0,
                "total": 101,
            }
        }
        assert client.payload_has_more_results(payload)

    def test_payload_has_more_results_false(self):
        client = AviationStackApiClient(threshold=100)
        payload = {
            "pagination": {
                "count": 100,
                "offset": 0,
                "total": 99,
            }
        }
        assert not client.payload_has_more_results(payload)

    def test_payload_has_more_results_malformed(self):
        client = AviationStackApiClient()
        payload = {}
        assert not client.payload_has_more_results(payload)
