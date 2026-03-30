import pytest
from unittest.mock import patch, MagicMock
from app import app
from utils.regex_utils import extract_shipment_fields
from models.shipment_schema import build_shipment_payload

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_extract_shipment_fields_valid():
    result = extract_shipment_fields("Order ORD123 with SHP456 delivery 2025-06-15")
    assert result["order_id"] == "ORD123"
    assert result["shipment_id"] == "SHP456"
    assert result["delivery_date"] == "2025-06-15"

def test_extract_shipment_fields_missing_order():
    result = extract_shipment_fields("SHP456 delivery 2025-06-15")
    assert result["order_id"] is None
    assert result["shipment_id"] == "SHP456"
    assert result["delivery_date"] == "2025-06-15"

def test_extract_shipment_fields_missing_all():
    result = extract_shipment_fields("no fields here")
    assert result["order_id"] is None
    assert result["shipment_id"] is None
    assert result["delivery_date"] is None

def test_build_shipment_payload():
    payload = build_shipment_payload("ORD123", "SHP456", "2025-06-15", "raw msg")
    assert payload == {
        "order_id": "ORD123",
        "shipment_id": "SHP456",
        "delivery_date": "2025-06-15",
        "raw_message": "raw msg",
    }

def test_update_shipment_missing_body(client):
    response = client.post("/update", json={})
    assert response.status_code == 400
    assert response.get_json()["status"] == "error"

def test_update_shipment_empty_message(client):
    response = client.post("/update", json={"message": "   "})
    assert response.status_code == 400

def test_update_shipment_missing_fields(client):
    response = client.post("/update", json={"message": "no fields here"})
    assert response.status_code == 422

def test_update_shipment_invalid_date(client):
    response = client.post("/update", json={"message": "ORD123 SHP456 2025-99-99"})
    assert response.status_code == 422

@patch("routes.shipment_routes.forward_shipment_data")
def test_update_shipment_success(mock_forward, client):
    mock_forward.return_value = {"forwarded": True, "status_code": 200, "error": None}
    response = client.post("/update", json={"message": "ORD123 SHP456 2025-06-15"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["order_id"] == "ORD123"
    assert data["shipment_id"] == "SHP456"
    assert data["delivery_date"] == "2025-06-15"
    assert data["forwarded"] is True

@patch("routes.shipment_routes.forward_shipment_data")
def test_update_shipment_forward_failure(mock_forward, client):
    mock_forward.return_value = {"forwarded": False, "status_code": None, "error": "timeout"}
    response = client.post("/update", json={"message": "ORD123 SHP456 2025-06-15"})
    assert response.status_code == 200
    assert response.get_json()["forwarded"] is False

def test_health(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
