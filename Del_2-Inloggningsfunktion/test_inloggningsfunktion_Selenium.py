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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pytest


# URL till applikationen som testas
URL = "https://www.saucedemo.com/"

@pytest.fixture
def driver():
    """
    Fixture som ansvarar för setup och teardown av WebDriver.
    Detta gör testerna oberoende av varandra, vilket är viktigt i CI-miljöer.
    """
    options = Options()

    # Headless-läge används för att testerna ska fungera i CI
    options.add_argument("--headless")

    # Nödvändiga inställningar för Linux-baserade CI-runners
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(URL)

    yield driver

    # Säkerställer att webbläsaren alltid stängs efter test
    driver.quit()


def login(driver, username, password):
    """
    Hjälpfunktion för inloggning.
    Minskar kodduplicering och gör testerna mer lättlästa.
    """
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

#----------------------------------------------------
#Positiva flöden
#----------------------------------------------------

@pytest.mark.parametrize(
    "username",
    [
        "standard_user",
        "problem_user",
        "performance_glitch_user",
        "error_user",
        "visual_user",
    ],
)

def test_anvandare_kan_logga_in_med_korrekta_uppgifter(driver, username):
    """
    Testfall verifiera att giltiga användare kan logga in
    """
    login(driver, username, "secret_sauce")

    # Vid lyckad inloggning hamnar man på inventory-sidan
    assert "inventory" in driver.current_url

#-----------------------------------------------------------
# Fel lösenord
#-----------------------------------------------------------

@pytest.mark.parametrize(
    "username",
    [
        "standard_user",
        "problem_user",
        "performance_glitch_user",
        "error_user",
        "visual_user",
    ],
)
def test_inloggning_misslyckas_vid_fel_losenord(driver, username):
    """
    Testfall verifieras att det inte är möjligt att logga med fel lösenord. Fel lösenordet blockeras
    och ge ett tydligt felmeddelande.
    """
    login(driver, username, "wrong_password")

    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert error.text == (
        "Epic sadface: Username and password do not match any user in this service"
    )

#--------------------------------------------------------------------
# Låsta användare
#--------------------------------------------------------------------
def test_last_anvandare_kan_inte_logga_in_med_ratt_losenord(driver):
    """
     Testfall kontrollerar att låsta användarkonton
     inte kan logga in med rätt lösenord.
    """
    login(driver, "locked_out_user", "secret_sauce")

    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert error.text == "Epic sadface: Sorry, this user has been locked out."

def test_last_anvandare_med_fel_losenord(driver):
    """
    Kontrollerar att låsta användarkonton inte kan logga in med ett annat lösenord.
    """
    login(driver, "locked_out_user", "secret_sauc")

    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert error.text == "Epic sadface: Username and password do not match any user in this service"

#---------------------------------------------------------------------
#Valibering av indata
#---------------------------------------------------------------------
def test_inloggning_med_tomma_falt(driver):
    """
    Validerar att inloggning inte tillåts när användarnamn anges men lösenordet saknar.
    """
    driver.find_element(By.ID, "login-button").click()

    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert error.text == "Epic sadface: Username is required"


def test_inloggning_med_anvandarnamn_utan_losenord(driver):
    """
     Validerar att inloggning inte tillåts när användarnamnet anges men lösenordet saknas
    """
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "login-button").click()

    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert error.text == "Epic sadface: Password is required"

def test_inloggning_med_losenord_utan_anvandarnamn(driver):
    """
     Validerar att inloggning inte tillåts när lösenordet anges men användarnamnet saknas
    """
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert error.text == "Epic sadface: Username is required"