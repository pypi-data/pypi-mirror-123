from unittest.mock import patch

import pytest

from compose.db2.configuration import Configuration
from compose.tests.mocks import kubernetes_mocks


@pytest.fixture
def configuration():
    with kubernetes_mocks.mock_kubernetes_v1_responses(), \
            patch('compose.db2.configuration.get_db2_major_version') as version:
        version.return_value = '11.1.4'
        configmap = {
            'account': 'some-account',
            'hostname': 'hostname',
            'id': 'thing-123',
            "peer_ips": '["1.2.3.4", "5.6.7.8"]',
            "peers": '["a-1", "a-2"]',
            'servicename': 'thingy',
            'type': 'db2',
            'compose_password': 'secret'
        }
        yield Configuration(sources=[configmap])

def test_placeholder():
    pass