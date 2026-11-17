
from fastapi.testclient import TestClient

from src.api import app

# Create a test client for our FastAPI application
client = TestClient(app)


def test_homepage():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "Running"
    assert data["message"] == "Welcome to Retail Sales Analytics API"


def test_sales_summary():
    response = client.get("/sales/summary")

    assert response.status_code == 200

    data = response.json()

    assert "product_sales" in data
    assert "freight_value" in data
    assert "total_including_freight" in data


def test_top_products_default():
    response = client.get("/products/top")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 10


def test_top_products_with_limit():
    response = client.get("/products/top?limit=5")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 5


def test_top_products_invalid_limit():
    response = client.get("/products/top?limit=0")

    assert response.status_code == 422


def test_monthly_sales():
    response = client.get("/sales/monthly")

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0


def test_categories():
    response = client.get("/categories")

    assert response.status_code == 200


def test_states():
    response = client.get("/states")

    assert response.status_code == 200


def test_payments():
    response = client.get("/payments")

    assert response.status_code == 200


def test_delivery():
    response = client.get("/delivery")

    assert response.status_code == 200


def test_order_status():
    response = client.get("/orders/status")

    assert response.status_code == 200

def test_top_products_maximum_limit():
    response = client.get("/products/top?limit=100")

    assert response.status_code == 200

    data = response.json()

    assert len(data) <= 100


def test_top_products_exceeds_maximum_limit():
    response = client.get("/products/top?limit=101")

    assert response.status_code == 422
    
