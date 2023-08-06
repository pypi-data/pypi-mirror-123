from unittest.mock import patch

import pytest

class MockResponse:
    def __init__(self, content, status_code=200):
        self.content = content
        self.status_code = status_code

    def json(self):
        return self.content

def test_placeholder():
    pass