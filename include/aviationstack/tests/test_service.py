import pytest
from aviationstack.client import AviationStackApiClient


@pytest.mark.module
@pytest.mark.service
@pytest.mark.live
class TestService:
    def test_aviation_stack_service_status(self):
        client = AviationStackApiClient(threshold=1)
        assert isinstance(client.get_all_flights("PHOG"), list)
