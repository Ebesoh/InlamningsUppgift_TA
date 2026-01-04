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


def test_successful_login_username1(driver):
    """Verifierar att användaren kan logga in med giltiga uppgifter.
    Detta är ett kritiskt användarflöde och lämpar sig väl för Selenium-testning."""

    login(driver, "standard_user", "secret_sauce")
    assert "inventory" in driver.current_url



def test_successful_login_username2(driver):
    """
    Verifierar att användaren kan logga in med giltiga uppgifter.
    Detta är ett kritiskt användarflöde och lämpar sig väl för Selenium-testning.
    """
    login(driver, "problem_user", "secret_sauce")
    assert "inventory" in driver.current_url

def test_successful_login_username3(driver):
    """
    Verifierar att användaren kan logga in med giltiga uppgifter.
    Detta är ett kritiskt användarflöde och lämpar sig väl för Selenium-testning.
    """
    login(driver, "performance_glitch_user", "secret_sauce")
    assert "inventory" in driver.current_url

def test_successful_login_username4(driver):
    """
    Verifierar att användaren kan logga in med giltiga uppgifter.
    Detta är ett kritiskt användarflöde och lämpar sig väl för Selenium-testning.
    """
    login(driver, "error_user", "secret_sauce")
    assert "inventory" in driver.current_url

def test_successful_login_username5(driver):
    """
    Verifierar att användaren kan logga in med giltiga uppgifter.
    Detta är ett kritiskt användarflöde och lämpar sig väl för Selenium-testning.
    """
    login(driver, "visual_user", "secret_sauce")
    assert "inventory" in driver.current_url


def test_wrong_password_username1(driver):

    """
    Säkerställer att systemet blockerar inloggning vid fel lösenord
    och ger användaren korrekt feedback.
    """
    login(driver,"standard_user", "wrong_password")
    error = driver.find_element(By.CSS_SELECTOR,"[data-test='error']")
    assert error.text == "Epic sadface: Username and password do not match any user in this service"

def test_wrong_password_username2(driver):
    """
    Säkerställer att systemet blockerar inloggning vid fel lösenord
    och ger användaren korrekt feedback.
    """
    login(driver, "problem_user", "wrong_password")
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert error.text == "Epic sadface: Username and password do not match any user in this service"

def test_wrong_password_username3(driver):
    """
    Säkerställer att systemet blockerar inloggning vid fel lösenord
    och ger användaren korrekt feedback.
    """
    login(driver, "performance_glitch_user", "wrong_password")
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert error.text == "Epic sadface: Username and password do not match any user in this service"

def test_wrong_password_username4(driver):
    """
    Säkerställer att systemet blockerar inloggning vid fel lösenord
    och ger användaren korrekt feedback.
    """
    login(driver, "error_user", "wrong_password")
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert error.text == "Epic sadface: Username and password do not match any user in this service"

def test_wrong_password_username5(driver):
    """
    Säkerställer att systemet blockerar inloggning vid fel lösenord
    och ger användaren korrekt feedback.
    """
    login(driver, "visual_user", "wrong_password")
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert error.text == "Epic sadface: Username and password do not match any user in this service"

def test_locked_user_givenpassword(driver):
    """
    Kontrollerar att låsta användarkonton inte kan logga in,
    vilket är ett viktigt säkerhetskrav.
    """
    login(driver, "locked_out_user", "secret_sauce")
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert error.text == "Epic sadface: Sorry, this user has been locked out."

def test_locked_user_wrongpassword(driver):
    """
    Kontrollerar att låsta användarkonton inte kan logga in,
    vilket är ett viktigt säkerhetskrav.
    """
    login(driver, "locked_out_user", "secret_sauc")
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert error.text == "Epic sadface: Username and password do not match any user in this service"


def test_empty_fields(driver):
    """
    Validerar att inloggning inte tillåts när obligatoriska fält saknas.
    """
    driver.find_element(By.ID, "login-button").click()
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert error.text == "Epic sadface: Username is required"

def test_username_without_password(driver):
    """
    Validerar att inloggning inte tillåts när användarnamn anges
    men lösenord saknas.
    """
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "login-button").click()

    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert error.text == "Epic sadface: Password is required"

def test_password_without_username(driver):
    """
    Validerar att inloggning inte tillåts när lösenord anges
    men användarnamn saknas.
    """
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert error.text == "Epic sadface: Username is required"