from selenium.webdriver.common.by import By

LOG_ICH = '//*[@id="rec1921710463"]/div/div/div[4]/a/img'

PROGRAMS = '//*[@id="molecule-176285426165558590"]/div[1]/a'

PAYMENT = '//*[@id="molecule-176285426165558590"]/div[2]/a/div/span'

ABOUT = '//*[@id="molecule-176285426165558590"]/div[3]/a/div/span'

CONTACTS = (By.LINK_TEXT, 'Контакты')

REVIEWS = "//span[@class='tn-atom__button-text' and text()='Отзывы']"

BLOG = "//span[@class='tn-atom__button-text' and text()='Блог']"

LANG_RU = "//span[@class='tn-atom__button-text' and text()='ru']"
LANG_DE = "//a[@href='/' and text()='de']"

CALLBACK = "//span[@class='tn-atom__button-text' and text()='ОБРАТНЫЙ ЗВОНОК']"

POPUP_TEXT = "//div[@class='tn-atom' and contains(., 'Запишитесь на') and contains(., 'карьерную консультацию')]"