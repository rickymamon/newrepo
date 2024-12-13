import pytest
from unittest.mock import patch
from datetime import datetime
from app import app, Client

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client