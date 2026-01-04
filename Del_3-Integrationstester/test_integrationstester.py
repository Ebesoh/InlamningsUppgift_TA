"""Del 3 - Integrationstester
För G –
● Skapa integrationstester som anropar https://fakestoreapi.com/.
● Testa:
○ En GET-förfrågan till /products returnerar statuskod 200.
● Skapa en GitHub Actions-pipeline som automatiskt kör dina tester vid varje push till
GitHub.
För VG –
Utöver kraven för G ska du även:
● Utöka integrationstesterna så att de validerar fler detaljer i API-svaren, till exempel:
○ Antalet produkter som returneras matchar det förväntade antalet.
○ En specifik produkt innehåller korrekta fält som title, price och category.
○ Ett specifikt produkt-ID returnerar rätt data."""

import requests

BASE_URL = "https://fakestoreapi.com"

def test_get_products_returns_200():
    response = requests.get(f"{BASE_URL}/products")
    assert response.status_code == 200


def test_products_count():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    assert len(products) == 20


def test_product_contains_required_fields():
    response = requests.get(f"{BASE_URL}/products")
    product = response.json()[0]

    assert "title" in product
    assert "price" in product
    assert "category" in product


def test_specific_product_id():
    response = requests.get(f"{BASE_URL}/products/1")
    product = response.json()

    assert product["id"] == 1
    assert "title" in product
    assert "price" in product
    assert "category" in product