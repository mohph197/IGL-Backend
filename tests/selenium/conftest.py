import pytest
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service

# Setting chrome driver fixture
@pytest.fixture()
def driver():
    load_dotenv()
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36')
    service = Service(os.getenv('CHROME_WEB_DRIVER_PATH'))
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

# Setting driver wait fixture
@pytest.fixture()
def wait(driver: webdriver.Chrome):
    return WebDriverWait(driver, 20)
