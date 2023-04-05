import pytest
from selenium import webdriver

@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('chromedriver.exe')
    pytest.driver.implicitly_wait(10)
    # Переход на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    pytest.driver.implicitly_wait(10)

    yield

    pytest.driver.quit()