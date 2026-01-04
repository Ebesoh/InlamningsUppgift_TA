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

import requests # Används för att skicka HTTP-förfrågningar till API:et

BASE_URL = "https://fakestoreapi.com"  # Bas-URL till fake Stor API. Ligger här för att enkelt kunna ändras på ett ställe

def test_get_products_returns_200():
    response = requests.get(f"{BASE_URL}/products")  #Skickar en GET-förfrågan
    assert response.status_code == 200 # Kontrollerar att API:et är tillgängligt och svarar korrekt. Statuskod 200 betyder "OK".


def test_products_count():
    response = requests.get(f"{BASE_URL}/products")  # Hämtar alla produkter från API:et
    products = response.json() # Omvandlar JSON-svaret till en Python-lista
    assert len(products) == 20  # Kontrollerar att API:et returnerar exakt 20 produkter


def test_product_contains_required_fields():
    response = requests.get(f"{BASE_URL}/products")  # Hämtar alla produkter från API:et
    product = response.json()[0]     # Tar ut den första produkten i listan

    # Kontrollerar att produkten innehåller nödvändiga fält
    # Dessa fält krävs för att applikationen ska fungera korrekt
    assert "title" in product
    assert "price" in product
    assert "category" in product


def test_specific_product_id():
    response = requests.get(f"{BASE_URL}/products/1") # Hämtar en specifik produkt baserat på ID
    product = response.json()

    assert product["id"] == 1 # Kontrollerar att rätt produkt returneras

    # Kontrollerar att rätt produkt returneras
    # Detta säkerställer konsekvent struktur i API:et
    assert "title" in product
    assert "price" in product
    assert "category" in product