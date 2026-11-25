from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

"""
Задание 1: Проверка наличия текста в iframe
Открыть страницу
Перейти по ссылке: https://bonigarcia.dev/selenium-webdriver-java/iframes.html.
Проверить наличие текста
Найти фрейм (iframe), в котором содержится искомый текст.
Переключиться в этот iframe.
Найти элемент, содержащий текст "semper posuere integer et senectus justo curabitur.".
Убедиться, что текст отображается на странице.
"""

def test_iframe_text():
    driver = webdriver.Chrome()
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/iframes.html")

    wait = WebDriverWait(driver, 15)

    try:
        # 1. Переключаемся внутрь iframe
        wait.until(
            EC.frame_to_be_available_and_switch_to_it("my-iframe")
        )

        # 2. Указываем искомый текст
        expected_text = "semper posuere integer et senectus justo curabitur."

        # 3. Ждём, пока текст появится внутри body
        wait.until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, "body"),
                expected_text
            )
        )

        # 4. Находим элемент с текстом
        body = driver.find_element(By.TAG_NAME, "body")

        # 5. Проверяем наличие текста
        assert expected_text in body.text

    finally:
        driver.quit()

"""
Задание 2: Тестирование Drag & Drop (Перетаскивание изображения в корзину)
Открыть страницу Drag & Drop Demo.
Перейти по ссылке: https://www.globalsqa.com/demo-site/draganddrop/.
Выполнить следующие шаги:
Захватить первую фотографию (верхний левый элемент).
Перетащить её в область корзины (Trash).
Проверить, что после перемещения:
В корзине появилась одна фотография.
В основной области осталось 3 фотографии.
Ожидаемый результат:
Фотография успешно перемещается в корзину.
Вне корзины остаются 3 фотографии.
"""


def test_drag_and_drop():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.globalsqa.com/demo-site/draganddrop/")
    wait = WebDriverWait(driver, 15)

    try:
        # Закрываем окно согласия cookies (актуально для Европы/Германии), если оно появилось
        try:
            consent = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".fc-cta-consent, #ez-accept-all"))
            )
            consent.click()
        except Exception:
            pass

        # 1. Находим ИМЕННО ВИДИМЫЙ iframe (на странице их несколько для разных вкладок)
        iframe = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[rel-title='Photo Manager'] iframe.demo-frame"))
        )
        driver.switch_to.frame(iframe)

        # 2. Ждем загрузки фотографий
        photos = wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#gallery li"))
        )

        # 3. Находим корзину
        trash = wait.until(
            EC.visibility_of_element_located((By.ID, "trash"))
        )

        # 4. Берем ПЕРВУЮ фотографию (индекс 0) и перетаскиваем
        first_photo = photos[0]
        actions = ActionChains(driver)
        actions.drag_and_drop(first_photo, trash).perform()

        # 5. Ждем, пока в галерее останется 3 элемента (надежнее, чем ждать #trash li)
        wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#gallery li")) == 3)

        # 6. Проверяем итоговое количество
        trash_count = len(driver.find_elements(By.CSS_SELECTOR, "#trash li"))
        gallery_count = len(driver.find_elements(By.CSS_SELECTOR, "#gallery li"))

        assert trash_count == 1, f"В корзине ожидалось 1 фото, но найдено: {trash_count}"
        assert gallery_count == 3, f"В галерее ожидалось 3 фото, но найдено: {gallery_count}"

    finally:
        driver.quit()