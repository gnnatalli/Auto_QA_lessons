''' Написать скрипт, который:

Открывает в браузере Firefox https://itcareerhub.de/ru

Переходит в раздел “Способы оплаты”

Делает скриншот этой секции страницы '''

import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_payment(driver):
    driver.get("https://itcareerhub.de/ru")

    payment = driver.find_element(By.LINK_TEXT, "Способы оплаты")
    payment.click()

    payment_section = driver.find_element(By.LINK_TEXT, "Способы оплаты")
    assert payment_section.text == "Способы оплаты"
    time.sleep(3)

    driver.save_screenshot("C:/Users/ICH/GIT/060326-ptm/ICH-KURS/Auto_qa_lessons/screenshot.png")
    time.sleep(3)