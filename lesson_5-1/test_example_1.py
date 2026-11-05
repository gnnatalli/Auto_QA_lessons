""" http://suninjuly.github.io/huge_form.html
Заполнить все поля ввода
Найти все input-поля типа text внутри формы.
Ввести в каждое поле значение "Hello".
Нажать кнопку Submit
Найти кнопку с классом btn btn-default.
Нажать на неё.
Дождаться появления Alert
Переключиться на всплывающее окно (alert).
Проверить текст Alert
Получить текст из alert.
Убедиться, что он содержит строку "Congrats, you've passed the task!". """


import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import math


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_fill_form_and_check_alert(browser):
    url = 'http://suninjuly.github.io/huge_form.html'
    browser.get(url)
    input_field = browser.find_element(By.TAG_NAME, "input")
    for field in input_fields:
        field.clear()
        field.send_keys("Hello")

