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

def test_get_client(client):
    mock_client = Client(
        id=1,
        first_name="John",
        last_name="Doe",
        address="Rizal",
        contact="098372764",
        email="ricky@gmail.com"
    )

    with patch("app.Client.query.get") as mock_get:
        mock_get.return_value = mock_client
        response = client.get("/client/1")
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["success"] is True
        assert json_data["data"]["id"] == 1


def test_delete_client(client):
    mock_client = Client(
        id=1,
        first_name="John",
        last_name="Doe",
        address="Rizal",
        contact="09123456789",
        email="rick716@gmail.com"
    )

    with patch("app.Client.query.get") as mock_get, \
         patch("app.db.session.delete"), \
         patch("app.db.session.commit"):
        mock_get.return_value = mock_client
        response = client.delete("/client/1")
        assert response.status_code == 204
        assert response.data == b''