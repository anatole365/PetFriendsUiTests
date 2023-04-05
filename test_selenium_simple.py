import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from settings import *
from selenium.webdriver.support import expected_conditions as EC


def test_show_my_pets():
    # Ввод email
    pytest.driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Ввод пароля
    pytest.driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаю на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Нажимаю на кнопку "Мои питомцы"
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Мои питомцы")]'))
    )
    pytest.driver.find_element(By.XPATH, '//a[contains(text(), "Мои питомцы")]').click()

    # Собираю инфу по именам, фото, породам и возростам питомцев
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]'))
    )
    names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')

    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]'))
    )
    species = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')

    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]'))
    )
    ages = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')

    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img'))
    )
    images = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')

    # Вывожу количество питомцев из статистики пользователя
    pets_amount = int(pytest.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]').text.split()[2])
    # Сравнивыю количество имен и количество питомцев из статистики пользователя
    assert len(names) == pets_amount

    # Считаю количество питомцев с фото
    count_images = 0
    for i in range(len(images)):
        if images[i].get_attribute('src'):
            count_images += 1
    # Убеждаюсь, что хотя бы у половины питомцев есть фото
    assert count_images >= pets_amount / 2

    # Считаю количество непустых элементов списков
    count_names = 0
    for i in range(len(names)):
        if names[i].text:
            count_names += 1
    count_species = 0
    for i in range(len(species)):
        if species[i].text:
            count_species += 1
    count_ages = 0
    for i in range(len(ages)):
        if ages[i].text:
            count_ages += 1
    # Убеждаюсь, что у всех питомцев есть имя, возраст и порода.
    assert count_names == count_species == count_ages == pets_amount

    # Вывожу все имена питомцев в список
    list_names = []
    for i in range(len(names)):
        list_names.append(names[i].text)
    # Убеждаюсь, что у всех питомцев разные имена.
    assert len(list_names) == len(set(list_names))

    # Составляю список описаний питомцев
    pet = []
    pets = []
    for i in range(len(names)):
        pet.append(names[i].text)
        pet.append(species[i].text)
        pet.append(ages[i].text)
        pets.append(tuple(pet))
        pet = []
    # Убеждаюсь, что в списке нет повторяющихся питомцев (у которых одинаковые имя, порода и возраст).
    assert len(pets) == len(set(pets))
