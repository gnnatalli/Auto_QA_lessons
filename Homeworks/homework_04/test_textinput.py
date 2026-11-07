import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


INPUT = (By.ID, "newButtonName")
BUTTON = (By.ID, "updatingButton")


def test_change_button_text(driver):
    # 1. Открываем страницу
    driver.get("http://uitestingplayground.com/textinput")

    # 2. Создаём явное ожидание
    wait = WebDriverWait(driver, 10)

    # 3. Находим поле ввода и вводим текст
    input_field = driver.find_element(*INPUT)
    input_field.send_keys("ITCH")
    time.sleep(5)

    # 4. Находим и нажимаем синюю кнопку
    button = driver.find_element(*BUTTON)
    button.click()
    time.sleep(5)

    # 5. Ждём, пока текст кнопки изменится на ITCH
    wait.until(
        EC.text_to_be_present_in_element(BUTTON, "ITCH")
    )

    # 6. Проверяем результат
    assert button.text == "ITCH"