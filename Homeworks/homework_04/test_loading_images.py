from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pytest


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_loading_images(driver):
    # 1. Открываем страницу
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/loading-images.html")

    # 2. Создаём явное ожидание
    wait = WebDriverWait(driver, 15)

    # 3. Ждём появления всех изображений и их полной загрузки
    wait.until(
        lambda driver: (
            len(images := driver.find_elements(By.TAG_NAME, "img")) > 0
            and all(
                driver.execute_script(
                    "return arguments[0].complete && arguments[0].naturalWidth > 0",
                    img
                )
                for img in images
            )
        )
    )

    # 4. Находим изображение award
    award_image = wait.until(
        lambda driver: driver.find_element(By.ID, "award")
    )

    # 5. Получаем значение атрибута alt
    alt_text = award_image.get_attribute("alt")

    # 6. Проверяем результат
    assert alt_text == "award"