from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pytest


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_about_button(driver):
    driver.get("https://itcareerhub.de/ru")
    about_button = driver.find_element(By.LINK_TEXT, 'О нас')  # Перейти на нужную странницу, здесь например "О нас"
    about_button.click()  # Нажать на нужную выбранную кнопку
    about_company = driver.find_element(By.LINK_TEXT, 'О компании')  # Перейти на следующую
    assert about_company.text == 'О компании'


# driver = webdriver.Chrome()
# time.sleep(5)
# driver.get("https://itcareerhub.de/ru")
# about_button = driver.find_element(By.LINK_TEXT, 'О нас') # Перейти на нужную странницу, здесь например "О нас"
# about_button.click() # Нажать на нужную выбранную кнопку
# time.sleep(3)









# driver.save_screenshot("./screenshot.png") # Делает скриншот
# time.sleep(3)











# driver.set_window_size(640, 480) # Размер окна выставляем
# time.sleep(3)
# driver.fullscreen_window() # Максимальный размер окна
# time.sleep(3)
# driver.minimize_window() # Минимальный размер окна
# time.sleep(3)

# driver.get("https://www.berlin.de/")
# time.sleep(3)

# driver.refresh() # обновление страницы
# time.sleep(3)
# driver.back()
# time.sleep(3)
# driver.forward()
