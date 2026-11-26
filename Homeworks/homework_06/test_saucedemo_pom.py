from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


"""
Напишите автоматизированный тест с использованием Page Object Model (POM), который выполняет следующие шаги:
Откройте сайт магазина: https://www.saucedemo.com/.
Авторизуйтесь как пользователь standard_user.
Добавьте в корзину товары:
Sauce Labs Backpack
Sauce Labs Bolt T-Shirt
Sauce Labs Onesie
Перейдите в корзину.
Нажмите Checkout.
Заполните форму своими данными:
Имя
Фамилия
Почтовый индекс
Прочтите со страницы итоговую стоимость (Total).
Закройте браузер.
Проверьте, что итоговая сумма равна $58.29.
Требования:
Использовать Page Object Model для организации кода.
Вынести все локаторы и методы работы со страницами в отдельные классы (Page Object).
Тест должен быть независимым и запускаться без предварительной подготовки данных.
"""
# --- Базовый класс ---
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find(locator).text

# --- Страница авторизации ---
class LoginPage(BasePage):
    URL = 'https://www.saucedemo.com/'
    USERNAME_INPUT = (By.ID, 'user-name')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'login-button')

    def open(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)


# --- Страница каталога товаров ---
class InventoryPage(BasePage):
    ADD_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    ADD_BOLT_TSHIRT = (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
    ADD_ONESIE = (By.ID, "add-to-cart-sauce-labs-onesie")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def add_products_to_cart(self):
        self.click(self.ADD_BACKPACK)
        self.click(self.ADD_BOLT_TSHIRT)
        self.click(self.ADD_ONESIE)

    def go_to_cart(self):
        self.click(self.CART_LINK)


# --- Страница корзины ---
class CartPage(BasePage):
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)


# --- Страница оформления заказа ---
class CheckoutPage(BasePage):
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")

    def fill_customer_info(self, first_name, last_name, postal_code):
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.type_text(self.POSTAL_CODE_INPUT, postal_code)
        self.click(self.CONTINUE_BUTTON)

    def get_total_price_text(self):
        return self.get_text(self.TOTAL_LABEL)


# --- Сам тест ---
def test_checkout_total_amount():
    chrome_options = Options()
    chrome_options.add_experimental_option(
        "prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False}
    )

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    total_text = ""

    try:
        # 1. Открываем сайт и логинимся
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        # 2. Добавляем 3 товара и переходим в корзину
        inventory_page = InventoryPage(driver)
        inventory_page.add_products_to_cart()
        inventory_page.go_to_cart()

        # 3. Переходим к оформлению
        cart_page = CartPage(driver)
        cart_page.proceed_to_checkout()

        # 4. Заполняем форму и получаем итоговую сумму
        checkout_page = CheckoutPage(driver)
        checkout_page.fill_customer_info("Ivan", "Ivanov", "01067")
        total_text = checkout_page.get_total_price_text()

    finally:
        # 5. Закрываем браузер до проверки
        driver.quit()

    # 6. Проверяем итоговую сумму
    assert total_text == "Total: $58.29", f"Ожидалось 'Total: $58.29', но получено '{total_text}'"