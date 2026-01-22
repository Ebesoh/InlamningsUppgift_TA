"""Del 2 – Inloggningsfunktion
På https://www.saucedemo.com/ finns en enkel inloggningsruta där användaren kan logga in.
Din uppgift är att skapa automatiserade testfall för denna funktion med hjälp av Selenium WebDriver.
Testerna ska vara tydligt strukturerade och täcka samtliga krav nedan.
För G – Grundläggande test
● Skapa ett testfall där inloggningen lyckas med korrekta användaruppgifter.
● Kontrollera att användaren loggas in och hamnar på startsidan efter lyckad inloggning.
För VG – Utökade tester(Samtliga G delar + utökade tester)
Utöver det grundläggande testet ska du även:
● Skapa ett testfall där fel användarnamn anges och verifiera att ett felmeddelande visas.
● Skapa ett testfall där fel lösenord anges och verifiera att ett felmeddelande visas.
https://education.systementor.se
OBS! Inkludera länk till ditt GitHub-repo i din rapport (del 1)!
OBS! OBS! Se till att GitHub-repot är Public och inte Private! Kommer jag inte repot får ni automatiskt underkänt."""

import pytest
from playwright.sync_api import sync_playwright,Page
from pytest_playwright.pytest_playwright import browser

URL = "https://www.saucedemo.com/"

@pytest.fixture()
def page() -> Page:
    """
       Fixture som ansvarar för setup och teardown av Playwright browser/page.
       Headless + CI-vänlig konfiguration.
       """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        context = browser.new_context()
        page = context.new_page()
        page.goto(URL)

        yield page
        browser.close()

def login(page: Page, username: str, password: str):
    """
    Hjälpfunktion för inloggning.
    """
    page.fill("#user-name", username)
    page.fill("#password", password)
    page.click("#login-button")


# ---------- Positiva fall ----------

@pytest.mark.parametrize(
    "username",
    [
        "standard_user",
        "problem_user",
        "performance_glitch_user",
        "error_user",
        "visual_user",
    ]
)
def test_anvandare_kan_logga_in_med_korrekta_uppgifter(page: Page, username):

    """ Testfall verifiera att giltiga användare kan logga in """
    login(page, username, "secret_sauce")
    assert "inventory" in page.url


# ---------- Fel lösenord ----------

@pytest.mark.parametrize(
    "username",
    [
        "standard_user",
        "problem_user",
        "performance_glitch_user",
        "error_user",
        "visual_user",
    ]
)
def test_inloggning_misslyckas_vid_fel_losenord(page: Page, username):
    """
       Testfall verifieras att det inte är möjligt att logga med fel lösenord. Fel lösenordet blockeras
       och ge ett tydligt felmeddelande.
       """
    login(page, username, "wrong_password")

    error = page.locator("[data-test='error']")
    assert error.text_content() == (
        "Epic sadface: Username and password do not match any user in this service"
    )


# ---------- Låst användare ----------

def test_last_anvandare_kan_inte_logga_in_med_ratt_losenord(page: Page):
    """
         Testfall kontrollerar att låsta användarkonton
         inte kan logga in med rätt lösenord.
        """
    login(page, "locked_out_user", "secret_sauce")

    error = page.locator("[data-test='error']")
    assert error.text_content() == (
        "Epic sadface: Sorry, this user has been locked out."
    )


def test_last_anvandare_med_fel_losenord(page: Page):
    """
    Kontrollerar att låsta användarkonton inte kan logga in med ett annat lösenord.
    """
    login(page, "locked_out_user", "secret_sauc")
    error = page.locator("[data-test='error']")
    assert error.text_content() == (
        "Epic sadface: Username and password do not match any user in this service"
    )


# ---------- Validering av indata ----------

def test_inloggning_med_tomma_falt(page: Page):
    """
    Validerar att inloggning inte tillåts när användarnamn anges men lösenordet saknar.
    """
    page.click("#login-button")
    error = page.locator("[data-test='error']")
    assert error.text_content() == "Epic sadface: Username is required"


def test_inloggning_med_anvandarnamn_utan_losenord(page: Page):
    """
    Validerar att inloggning inte tillåts när användarnamnet anges men lösenordet saknas
    """
    page.fill("#user-name", "standard_user")
    page.click("#login-button")
    error = page.locator("[data-test='error']")
    assert error.text_content() == "Epic sadface: Password is required"


def test_inloggning_med_losenord_utan_anvandarnamn(page: Page):
    """
    Validerar att inloggning inte tillåts när lösenordet anges men användarnamnet saknas
    """
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    error = page.locator("[data-test='error']")
    assert error.text_content() == "Epic sadface: Username is required"