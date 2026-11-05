import time

import pytest
from cffi.cffi_opcode import CLASS_NAME
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from urls import HOMEPAGE
from locators import LOG_ICH, PROGRAMS, PAYMENT, ABOUT, CONTACTS, REVIEWS, BLOG, LANG_RU, LANG_DE, CALLBACK, POPUP_TEXT
"""Написать автотест с использованием Python и Pytest, который:
Открывает https://itcareerhub.de/ru
Проверяет, что на странице отображаются:
Логотип ITCareerHub
Ссылка “Программы”
Ссылка “Способы оплаты”
Ссылка “О нас”
Ссылка “Контакты”
Ссылка “Отзывы”
Ссылка “Блог”
Кнопки переключения языка (ru и de)
Кликнуть по разделу “Контакты”
Кликнуть по кнопке “Обратный звонок”
Проверить что текст “Запишитесь на бесплатную карьерную консультацию” отображается во всплывающем окне.
"""

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get(HOMEPAGE)
    yield driver
    driver.quit()



def test_itcareerhub(driver):
    wait = WebDriverWait(driver, 10)
    # 1. Проверяем логотип "ITCareerHub"
    log_ich = driver.find_element(By.XPATH, LOG_ICH)
    assert log_ich.is_displayed() is True

    # 2. Проверяем ссылку "Программы"
    programs = driver.find_element(By.XPATH, PROGRAMS)
    assert programs.is_displayed() is True

    # 3. Проверяем ссылку "Способы оплаты"
    payment = driver.find_element(By.XPATH, PAYMENT)
    assert payment.is_displayed()

    # 4. Проверяем ссылку "О нас"
    about = driver.find_element(By.XPATH, ABOUT)
    assert about.is_displayed()

    # 5. Наводим курсор на О нас
    ActionChains(driver).move_to_element(about).perform()

    # Проверяем ссылку "Контакты"
    contacts = wait.until(
        EC.visibility_of_element_located(CONTACTS)
    )
    assert contacts.is_displayed()

    # 6. Проверяем ссылку "Отзывы"
    reviews = driver.find_element(By.XPATH, REVIEWS)
    assert reviews.is_displayed()

    # 7. Проверяем ссылку "Блог"
    blog = driver.find_element(By.XPATH, BLOG)
    assert blog.is_displayed()

    # 8. Проверяем переключатель языка ru
    lang_ru = driver.find_element(By.XPATH, LANG_RU)
    assert lang_ru.is_displayed()

    # 9. Проверяем переключатель языка de
    lang_de = driver.find_element(By.XPATH, LANG_DE)
    assert lang_de.is_displayed()

    #10. Кликнуть по разделу “Контакты”
    # Наводим курсор на О нас
    ActionChains(driver).move_to_element(about).perform()

    # Проверяем ссылку Контакты
    contacts = wait.until(
        EC.visibility_of_element_located(CONTACTS)
    )
    assert contacts.is_displayed()

    # Прокручиваем страницу к ссылке "Контакты"
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        contacts
    )

    # Наводим курсор на ссылку
    ActionChains(driver).move_to_element(contacts).perform()

    # Кликаем по ссылке "Контакты"
    contacts.click()

    # 11. Проверяем и нажимаем кнопку "Обратный звонок"
    callback = wait.until(
        EC.element_to_be_clickable((By.XPATH, CALLBACK))
    )
    callback.click()

    # 12. Проверяем текст во всплывающем окне
    popup_text = wait.until(
        EC.visibility_of_element_located((By.XPATH, POPUP_TEXT))
    )

    assert popup_text.is_displayed()
    assert "Запишитесь на бесплатную карьерную консультацию" in popup_text.text

