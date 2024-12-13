import pytest
from unittest.mock import patch
from datetime import datetime
from app import app, Client

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_clients(client):
    # Mocked clients
    mock_clients = [
        Client(
            id=1,
            first_name="John",
            last_name="Doe",
            address="Rizal",
            contact="098372764",
            email="ricky@gmail.com"
        ),
        Client(
            id=2,
            first_name="Ricky",
            last_name="Smith",
            address="Pal",
            contact="09837277834",
            email="ricky16@gmail.com"
        ),
    ]
    
    with patch("app.Client.query.all") as mock_all:
        mock_all.return_value = mock_clients
        response = client.get("/client")
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["success"] is True
        assert len(json_data["data"]) == len(mock_clients)