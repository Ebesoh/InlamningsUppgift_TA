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

def test_get_products_returns_200(): # Testfall kontrollerar att API:et är tillgängligt och svarar korrekt. Statuskod 200 betyder "OK".
    response = requests.get(f"{BASE_URL}/products")  #Skickar en GET-förfrågan

    assert response.status_code == 200 # Kontrollerar att API:et är tillgängligt och svarar korrekt. Statuskod 200 betyder "OK".


def test_products_response_is_json(): #  Testfall: Kontrollera att API-svaret är i JSON-format
    response = requests.get(f"{BASE_URL}/products")

    assert response.headers["Content-Type"].startswith("application/json") #kontrollera att content-Type börjar med 'application/json'



def test_products_count_is_20(): # Testfall: Kontrollera att API:et returnerar rätt antal produkter.
    response = requests.get(f"{BASE_URL}/products")  # Hämtar alla produkter från API:et
    products = response.json() # Omvandlar JSON-svaret till en Python-lista

    assert len(products) == 20 # Kontrollerar att API:et returnerar exakt 20 produkter


def test_specific_product_contains_required_fields(): #Testfall: Kontrollera att en produkt innehåller nödvändiga fält.
    response = requests.get(f"{BASE_URL}/products")  # Hämtar alla produkter från API:et
    product = response.json()[0]                     # Tar ut den första produkten i listan

    # Kontrollerar att produkten innehåller nödvändiga fält (id, title, price and category)
    # Dessa fält krävs för att applikationen ska fungera korrekt
    assert "id" in product
    assert "title" in product
    assert "price" in product
    assert "category" in product


def test_product_field_types(): # Testfall kontrollera att fälten i en product har rätt datatyper
    response = requests.get(f"{BASE_URL}/products")
    product = response.json()[0]

    assert isinstance(product["id"], int)
    assert isinstance(product["title"], str)
    assert isinstance(product["price"], (int, float))
    assert isinstance(product["category"], str)


def test_specific_product_id_is_correct(): # Testfall: Kontrollera att rätt produkt returneras för ID 1.
    response = requests.get(f"{BASE_URL}/products/1") # Hämtar en specifik produkt baserat på ID
    product = response.json()

    assert product["id"] == 1 # Kontrollerar att rätt produkt returneras


def test_product_price_is_positive(): # Testfall: Kontrollera att produktens pris är större än 0.
    response = requests.get(f"{BASE_URL}/products/1") # Hämtar en specifik produkt baserat på ID
    product = response.json()

    assert product["price"] > 0 # Kontrollerar att produktens pris är större än 0


def test_all_products_have_unique_ids(): #Testfall: Kontrollera att alla produkter har unika ID:n.
    response = requests.get(f"{BASE_URL}/products") #Skickar en GET-förfrågan
    products = response.json()  # Omvandlar API-svaret från JSON till en Python-lista

    ids = [product["id"] for product in products]  # Samlar alla produkt-ID:n i en lista
    assert len(ids) == len(set(ids)) # Jämför antal ID:n med antal unika ID:n